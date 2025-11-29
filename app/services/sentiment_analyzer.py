from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer
import spacy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import logging
import numpy as np
from app.config import settings
import re

class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.nlp = None
        self.spanish_sentiment_words = {
            'positive': ['excelente', 'bueno', 'perfecto', 'genial', 'contento', 'satisfecho', 'rápido', 'eficiente', 'útil', 'recomiendo'],
            'negative': ['malo', 'horrible', 'terrible', 'lento', 'error', 'falla', 'problema', 'inaceptable', 'pésimo', 'decepcionado']
        }
        self.load_models()

    def load_models(self):
        """Cargar modelos de ML o usar TextBlob como fallback"""
        try:
            self.model = joblib.load(settings.SENTIMENT_MODEL_PATH)
            self.vectorizer = joblib.load(settings.VECTORIZER_MODEL_PATH)
            logging.info("✅ Modelos de sentimiento cargados exitosamente")
        except:
            logging.warning("⚠️ No se pudieron cargar modelos de ML, usando análisis basado en reglas para español")

        try:
            self.nlp = spacy.load("es_core_news_sm")
        except:
            logging.warning("⚠️ No se pudo cargar spaCy para análisis avanzado")

    def analyze_spanish_sentiment(self, text: str) -> dict:
        """Análisis de sentimiento en español usando reglas y palabras clave"""
        text_lower = text.lower()
        
        # Contar palabras positivas y negativas
        positive_count = sum(1 for word in self.spanish_sentiment_words['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.spanish_sentiment_words['negative'] if word in text_lower)
        
        # Palabras intensificadoras
        intensifiers = ['muy', 'mucho', 'realmente', 'extremadamente', 'totalmente']
        intensifier_count = sum(1 for word in intensifiers if word in text_lower)
        
        # Calcular score basado en proporciones
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return self.get_neutral_sentiment()
        
        # Score base
        base_sentiment = (positive_count - negative_count) / total_sentiment_words
        
        # Ajustar por intensificadores
        intensity_boost = min(intensifier_count * 0.2, 0.6)
        if base_sentiment > 0:
            final_sentiment = min(base_sentiment + intensity_boost, 1.0)
        elif base_sentiment < 0:
            final_sentiment = max(base_sentiment - intensity_boost, -1.0)
        else:
            final_sentiment = 0.0
        
        # Determinar etiqueta y confianza
        confidence = min(abs(final_sentiment) + 0.3, 1.0)  # Confianza base
        
        if final_sentiment > 0.1:
            label = "positivo"
            confidence = max(confidence, abs(final_sentiment))
        elif final_sentiment < -0.1:
            label = "negativo" 
            confidence = max(confidence, abs(final_sentiment))
        else:
            label = "neutral"
            confidence = 0.7  # Mayor confianza en neutral
            
        return {
            "sentiment": round(final_sentiment, 3),
            "label": label,
            "confidence": round(confidence, 3),
            "positive_score": max(0, final_sentiment),
            "negative_score": max(0, -final_sentiment),
            "method": "spanish_rules"
        }

    def analyze_with_textblob(self, text: str) -> dict:
        """Análisis de sentimiento usando TextBlob (inglés)"""
        try:
            # Limpiar texto para TextBlob
            cleaned_text = re.sub(r'[^\w\s]', '', text)
            blob = TextBlob(cleaned_text, analyzer=PatternAnalyzer())
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # TextBlob funciona mejor con inglés, así que el score será más neutral
            # Para español, ajustamos el threshold
            if polarity > 0.2:
                label = "positivo"
                confidence = polarity
            elif polarity < -0.2:
                label = "negativo"
                confidence = abs(polarity)
            else:
                label = "neutral"
                confidence = 0.6
                
            # Ajustar confidence para español
            confidence = confidence * 0.7  # Reducir confianza para texto en español
            
            return {
                "sentiment": round(polarity, 3),
                "label": label,
                "confidence": round(confidence, 3),
                "positive_score": max(0, polarity),
                "negative_score": max(0, -polarity),
                "subjectivity": round(subjectivity, 3),
                "method": "textblob"
            }
        except Exception as e:
            logging.error(f"Error en TextBlob: {e}")
            return self.get_neutral_sentiment()

    def get_neutral_sentiment(self) -> dict:
        """Retornar sentimiento neutral por defecto"""
        return {
            "sentiment": 0.0,
            "label": "neutral",
            "confidence": 0.5,
            "positive_score": 0.0,
            "negative_score": 0.0,
            "method": "fallback"
        }

    def analyze_sentiment(self, text: str) -> dict:
        """Analizar sentimiento del texto con prioridad para español"""
        # Primero intentar con nuestro método en español
        spanish_result = self.analyze_spanish_sentiment(text)
        
        # Si nuestro método detecta sentimiento claro, usarlo
        if abs(spanish_result["sentiment"]) > 0.3 and spanish_result["confidence"] > 0.6:
            return spanish_result
        
        # Si no, usar TextBlob como respaldo
        textblob_result = self.analyze_with_textblob(text)
        
        # Combinar resultados si es necesario
        if abs(spanish_result["sentiment"]) > 0.1:
            # Ponderar ambos resultados
            combined_sentiment = (spanish_result["sentiment"] * 0.7 + 
                                textblob_result["sentiment"] * 0.3)
            combined_confidence = (spanish_result["confidence"] + 
                                 textblob_result["confidence"]) / 2
            
            if combined_sentiment > 0.1:
                label = "positivo"
            elif combined_sentiment < -0.1:
                label = "negativo"
            else:
                label = "neutral"
                
            return {
                "sentiment": round(combined_sentiment, 3),
                "label": label,
                "confidence": round(combined_confidence, 3),
                "positive_score": max(0, combined_sentiment),
                "negative_score": max(0, -combined_sentiment),
                "method": "combined"
            }
        
        return textblob_result