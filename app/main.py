from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from app.models import TextAnalysisRequest, VectorizationResponse, SentimentResponse, TokenizationResponse, LinguisticFeatures
from app.services.text_vectorizer import TextVectorizer
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.text_tokenizer import TextTokenizer
from app.database import mongodb
from app.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MS-Text-Analysis-Service",
    description="Microservicio de análisis de texto para NLP - Vectorización, Sentimiento y Tokenización",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
text_vectorizer = TextVectorizer()
sentiment_analyzer = SentimentAnalyzer()
text_tokenizer = TextTokenizer()

@app.post("/api/text/vectorize", response_model=VectorizationResponse)
async def vectorize_text(request: TextAnalysisRequest, method: str = "tfidf", reduce_dims: bool = True):
    """Endpoint para vectorizar texto"""
    try:
        result = text_vectorizer.vectorize_text(
            request.text, 
            method=method, 
            reduce_dimensions=reduce_dims
        )
        
        # Guardar en log
        if request.ticket_id:
            analysis_log = {
                "ticket_id": request.ticket_id,
                "timestamp": datetime.now(),
                "action": "vectorization",
                "details": {
                    "method": result["method"],
                    "dimensions": result["dimensions"],
                    "vector_sample": result["vector"][:10] if result["vector"] else []
                }
            }
            collection = mongodb.get_collection(settings.TEXT_ANALYSIS_COLLECTION)
            collection.insert_one(analysis_log)
        
        return VectorizationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error en vectorización: {e}")
        raise HTTPException(status_code=500, detail=f"Error en vectorización: {str(e)}")

@app.post("/api/text/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: TextAnalysisRequest):
    """Endpoint para analizar sentimiento del texto"""
    try:
        result = sentiment_analyzer.analyze_sentiment(request.text)
        
        # Guardar en log
        if request.ticket_id:
            analysis_log = {
                "ticket_id": request.ticket_id,
                "timestamp": datetime.now(),
                "action": "sentiment_analysis",
                "details": result
            }
            collection = mongodb.get_collection(settings.TEXT_ANALYSIS_COLLECTION)
            collection.insert_one(analysis_log)
        
        return SentimentResponse(**result)
        
    except Exception as e:
        logger.error(f"Error en análisis de sentimiento: {e}")
        raise HTTPException(status_code=500, detail=f"Error en análisis de sentimiento: {str(e)}")

@app.post("/api/text/tokenize", response_model=TokenizationResponse)
async def tokenize_text(
    request: TextAnalysisRequest, 
    remove_stopwords: bool = True, 
    use_lemmas: bool = False
):
    """Endpoint para tokenizar y limpiar texto"""
    try:
        result = text_tokenizer.tokenize(
            request.text, 
            remove_stopwords=remove_stopwords, 
            use_lemmas=use_lemmas
        )
        
        # Guardar en log
        if request.ticket_id:
            analysis_log = {
                "ticket_id": request.ticket_id,
                "timestamp": datetime.now(),
                "action": "tokenization",
                "details": {
                    "token_count": result["token_count"],
                    "original_length": result["original_length"],
                    "remove_stopwords": remove_stopwords,
                    "use_lemmas": use_lemmas
                }
            }
            collection = mongodb.get_collection(settings.TEXT_ANALYSIS_COLLECTION)
            collection.insert_one(analysis_log)
        
        return TokenizationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error en tokenización: {e}")
        raise HTTPException(status_code=500, detail=f"Error en tokenización: {str(e)}")

@app.post("/api/text/linguistic-features")
async def get_linguistic_features(request: TextAnalysisRequest):
    """Endpoint para extraer características lingüísticas"""
    try:
        features = text_tokenizer.extract_linguistic_features(request.text)
        
        return LinguisticFeatures(**features)
        
    except Exception as e:
        logger.error(f"Error extrayendo características: {e}")
        raise HTTPException(status_code=500, detail=f"Error extrayendo características: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check del servicio"""
    return {
        "status": "healthy",
        "service": "MS-Text-Analysis-Service",
        "timestamp": datetime.now(),
        "features": [
            "vectorization",
            "sentiment_analysis", 
            "tokenization",
            "linguistic_features"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)