import spacy
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import logging

# Descargar recursos de NLTK (solo primera vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextTokenizer:
    def __init__(self):
        self.spanish_stopwords = set(stopwords.words('spanish'))
        self.stemmer = SnowballStemmer('spanish')
        self.nlp = None
        self.load_spacy_model()

    def load_spacy_model(self):
        """Cargar modelo de spaCy para español"""
        try:
            self.nlp = spacy.load("es_core_news_sm")
            logging.info("✅ Modelo spaCy cargado exitosamente")
        except OSError:
            logging.warning("⚠️ No se pudo cargar el modelo spaCy, usando NLTK")
            self.nlp = None

    def clean_text(self, text: str) -> str:
        """Limpieza mejorada del texto con manejo de encoding"""
        # Convertir a minúsculas
        text = text.lower()
        
        # Corregir encoding issues comunes
        try:
            text = text.encode('utf-8', 'ignore').decode('utf-8')
        except:
            # Si hay problemas con encoding, intentar limpiar caracteres no ASCII
            text = ''.join(char for char in text if ord(char) < 128)
        
        # Eliminar caracteres especiales pero mantener letras, números, acentos y signos básicos
        text = re.sub(r'[^a-zA-ZáéíóúñüÁÉÍÓÚÑÜ0-9\s.,!?;:()\-]', '', text)
        
        # Eliminar espacios extra
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def tokenize_with_spacy(self, text: str) -> dict:
        """Tokenización avanzada con spaCy"""
        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_space]
        lemmas = [token.lemma_ for token in doc if not token.is_space and not token.is_punct]
        
        return {
            "tokens": tokens,
            "lemmas": lemmas,
            "cleaned_text": " ".join(tokens)
        }

    def tokenize_with_nltk(self, text: str) -> dict:
        """Tokenización con NLTK"""
        tokens = word_tokenize(text, language='spanish')
        # Filtrar tokens (quitar puntuación y espacios)
        tokens = [token for token in tokens if token.isalnum()]
        lemmas = [self.stemmer.stem(token) for token in tokens]
        
        return {
            "tokens": tokens,
            "lemmas": lemmas,
            "cleaned_text": " ".join(tokens)
        }

    def tokenize(self, text: str, remove_stopwords: bool = True, use_lemmas: bool = False) -> dict:
        """Tokenizar texto con opciones avanzadas"""
        # Limpiar texto
        cleaned_text = self.clean_text(text)
        
        # Elegir método de tokenización
        if self.nlp:
            result = self.tokenize_with_spacy(cleaned_text)
        else:
            result = self.tokenize_with_nltk(cleaned_text)
        
        # Remover stopwords si se solicita
        if remove_stopwords:
            result["tokens"] = [token for token in result["tokens"] if token not in self.spanish_stopwords]
            if result["lemmas"]:
                result["lemmas"] = [lemma for lemma in result["lemmas"] if lemma not in self.spanish_stopwords]
        
        # Usar lemmas en lugar de tokens si se solicita
        final_tokens = result["lemmas"] if use_lemmas and result["lemmas"] else result["tokens"]
        
        return {
            "tokens": final_tokens,
            "original_length": len(text),
            "token_count": len(final_tokens),
            "cleaned_text": result["cleaned_text"],
            "lemmas": result["lemmas"] if use_lemmas else None
        }

    def extract_linguistic_features(self, text: str) -> dict:
        """Extraer características lingüísticas del texto"""
        # Tokenizar oraciones
        sentences = sent_tokenize(text, language='spanish')
        words = word_tokenize(text, language='spanish')
        words = [word for word in words if word.isalnum()]
        
        # Calcular métricas
        word_count = len(words)
        sentence_count = len(sentences)
        unique_words = len(set(words))
        
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        lexical_diversity = unique_words / word_count if word_count > 0 else 0
        
        # Score de legibilidad simple (para español)
        readability_score = self.calculate_readability(text, word_count, sentence_count)
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_word_length": round(avg_word_length, 2),
            "unique_words": unique_words,
            "lexical_diversity": round(lexical_diversity, 3),
            "readability_score": round(readability_score, 2)
        }

    def calculate_readability(self, text: str, word_count: int, sentence_count: int) -> float:
        """Calcular score de legibilidad para español"""
        if sentence_count == 0 or word_count == 0:
            return 0
        
        avg_sentence_length = word_count / sentence_count
        # Fórmula simplificada de legibilidad
        readability = 206.84 - (1.02 * avg_sentence_length) - (0.6 * (word_count / sentence_count))
        return max(0, min(100, readability))