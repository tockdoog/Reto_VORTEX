import joblib
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
import logging
from app.config import settings

# Lista personalizada de stop words en español
SPANISH_STOP_WORDS = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 
    'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 
    'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 
    'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'estados', 
    'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 
    'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 
    'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 
    'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 
    'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías',
    'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 
    'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 
    'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 
    'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 
    'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 
    'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 
    'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 
    'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 
    'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 
    'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 
    'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 
    'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 
    'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 
    'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 
    'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 
    'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 
    'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 
    'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 
    'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 
    'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 
    'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 
    'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 
    'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 
    'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 
    'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 
    'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 
    'tenidos', 'tenidas', 'tened'
]

class TextVectorizer:
    def __init__(self):
        self.vectorizer = None
        self.load_vectorizer()

    def load_vectorizer(self):
        """Cargar vectorizador que no requiere entrenamiento"""
        try:
            # Intentar cargar modelos pre-entrenados si existen
            self.vectorizer = joblib.load(settings.VECTORIZER_MODEL_PATH)
            logging.info("✅ Modelo de vectorización pre-entrenado cargado")
        except:
            # Usar HashingVectorizer que no necesita entrenamiento
            logging.info("✅ Usando HashingVectorizer (no requiere entrenamiento)")
            self.vectorizer = HashingVectorizer(
                n_features=1024,
                stop_words=SPANISH_STOP_WORDS,  # Usar nuestra lista personalizada
                ngram_range=(1, 2),
                norm='l2',
                alternate_sign=False
            )

    def vectorize_tfidf(self, text: str, reduce_dimensions: bool = True) -> dict:
        """Vectorizar texto usando HashingVectorizer (equivalente a TF-IDF)"""
        try:
            # HashingVectorizer no necesita fit, puede transformar directamente
            vector = self.vectorizer.transform([text]).toarray()[0]
            method = "HashingVectorizer"
            
            # Reducir dimensionalidad si se solicita
            if reduce_dimensions and len(vector) > 100:
                # Reducción simple: tomar cada 10mo elemento para vector más pequeño
                reduced_vector = vector[::10]
                if len(reduced_vector) < 10:  # Asegurar tamaño mínimo
                    reduced_vector = vector[:100]
                method += " + Reduced"
                final_vector = reduced_vector.tolist()
            else:
                final_vector = vector.tolist()
            
            return {
                "vector": final_vector,
                "dimensions": len(final_vector),
                "method": method,
                "features": None  # HashingVectorizer no tiene nombres de características
            }
            
        except Exception as e:
            logging.error(f"Error en vectorización TF-IDF: {e}")
            # Fallback extremo - vector basado en características del texto
            return self.create_fallback_vector(text)

    def vectorize_count(self, text: str, ngram_range: tuple = (1, 1)) -> dict:
        """Vectorizar texto usando enfoque tipo Count"""
        try:
            # Usar HashingVectorizer con configuración tipo count
            count_vectorizer = HashingVectorizer(
                n_features=512,
                stop_words=SPANISH_STOP_WORDS,  # Usar nuestra lista personalizada
                ngram_range=ngram_range,
                norm=None,  # Sin normalización para parecerse a count
                alternate_sign=False
            )
            
            vector = count_vectorizer.transform([text]).toarray()[0]
            
            return {
                "vector": vector.tolist(),
                "dimensions": len(vector),
                "method": f"CountVectorizer {ngram_range}",
                "features": None
            }
        except Exception as e:
            logging.error(f"Error en count vectorization: {e}")
            return self.create_fallback_vector(text)

    def create_fallback_vector(self, text: str) -> dict:
        """Crear vector de fallback basado en características del texto"""
        # Características básicas del texto
        length = len(text)
        word_count = len(text.split())
        unique_chars = len(set(text.lower()))
        digit_count = sum(c.isdigit() for c in text)
        upper_count = sum(c.isupper() for c in text)
        
        # Vector simple basado en estas características
        vector = [
            length / 1000.0,  # Longitud normalizada
            word_count / 100.0,  # Conteo de palabras normalizado
            unique_chars / 100.0,  # Caracteres únicos
            digit_count / 10.0,  # Dígitos
            upper_count / 10.0,  # Mayúsculas
            text.count('!'),  # Signos de exclamación
            text.count('?'),  # Signos de interrogación
            text.count('.')   # Puntos
        ]
        
        # Rellenar hasta 10 dimensiones si es necesario
        while len(vector) < 10:
            vector.append(0.0)
            
        return {
            "vector": vector[:10],  # Mantener en 10 dimensiones
            "dimensions": 10,
            "method": "Fallback_Features",
            "features": ["length", "word_count", "unique_chars", "digits", "uppercase", "exclamations", "questions", "periods"]
        }

    def vectorize_text(self, text: str, method: str = "tfidf", **kwargs) -> dict:
        """Vectorizar texto usando el método especificado"""
        # Limpiar y preparar texto
        text = str(text).strip()
        if not text:
            return self.create_fallback_vector("empty")
            
        method = method.lower()
        
        if method == "tfidf":
            return self.vectorize_tfidf(text, **kwargs)
        elif method == "count":
            return self.vectorize_count(text, **kwargs)
        else:
            logging.warning(f"Método {method} no reconocido, usando TF-IDF")
            return self.vectorize_tfidf(text, **kwargs)