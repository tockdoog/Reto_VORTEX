from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from app.models import TextAnalysisRequest, VectorizationResponse, SentimentResponse, TokenizationResponse, LinguisticFeatures, SecurityResponse
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

@app.post("/api/security/detect-phishing", response_model=SecurityResponse)
async def detect_phishing(request: TextAnalysisRequest):
    try:
        text = request.text
        threats = []
        risk = 0
        patterns = [
            r"verifique\s+su\s+cuenta",
            r"actualizaci[óo]n\s+urgente",
            r"haga\s+click\s+aqu[ií]",
            r"contrase[ñn]a",
            r"confirmar\s+(identidad|cuenta)",
            r"suspendid[ao]",
            r"iniciar\s+ses[ií]on",
            r"enlace\s+de\s+verificaci[óo]n",
            r"tarjeta\s+de\s+cr[eé]dito",
            r"banco|proveedor|paypal"
        ]
        for p in patterns:
            import re
            if re.search(p, text, flags=re.IGNORECASE):
                threats.append(p)
                risk += 2
        url_patterns = [r"https?://[\w.-]*", r"\bbit\.ly\b|\btinyurl\.com\b|\bow\.ly\b"]
        for up in url_patterns:
            import re
            if re.search(up, text, flags=re.IGNORECASE):
                threats.append(up)
                risk += 2
        import re
        emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
        if emails:
            threats.append("email_presence")
            risk += 1
        html_link = re.search(r"<a\s+href=", text, flags=re.IGNORECASE) is not None
        if html_link:
            threats.append("html_link")
            risk += 1
        is_safe = risk < 3
        anonymized = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]", text)
        anonymized = re.sub(r"https?://[\w./-]*", "[url]", anonymized)
        try:
            collection = mongodb.get_collection(settings.TEXT_ANALYSIS_COLLECTION)
            collection.insert_one({
                "timestamp": datetime.now(),
                "action": "security_phishing",
                "ticket_id": request.ticket_id,
                "threats": threats,
                "risk": risk,
                "anonymized_text": anonymized
            })
        except Exception:
            pass
        return SecurityResponse(isSafe=is_safe, threatsDetected=threats, anonymizedText=anonymized)
    except Exception as e:
        logger.error(f"Error en detección de phishing: {e}")
        raise HTTPException(status_code=500, detail=f"Error en detección de phishing: {str(e)}")

@app.post("/api/security/anonymize-data")
async def anonymize_data(request: TextAnalysisRequest):
    try:
        import re
        text = request.text
        anonymized = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]", text)
        anonymized = re.sub(r"https?://[\w./-]*", "[url]", anonymized)
        anonymized = re.sub(r"\b\+?\d[\d\s-]{7,}\b", "[phone]", anonymized)
        anonymized = re.sub(r"\b(pass|password|contrase[ñn]a)\s*[:=]\s*\S+", "[credential]", anonymized, flags=re.IGNORECASE)
        try:
            collection = mongodb.get_collection(settings.TEXT_ANALYSIS_COLLECTION)
            collection.insert_one({
                "timestamp": datetime.now(),
                "action": "security_anonymize",
                "ticket_id": request.ticket_id,
                "anonymized_text": anonymized
            })
        except Exception:
            pass
        return {"anonymizedText": anonymized}
    except Exception as e:
        logger.error(f"Error en anonimización: {e}")
        raise HTTPException(status_code=500, detail=f"Error en anonimización: {str(e)}")

@app.get("/api/security/threats")
async def get_threats():
    try:
        collection = mongodb.get_collection(settings.TEXT_ANALYSIS_COLLECTION)
        cursor = collection.find({"action": "security_phishing"}).sort("timestamp", -1).limit(50)
        items = []
        for doc in cursor:
            items.append({
                "timestamp": doc.get("timestamp"),
                "ticket_id": doc.get("ticket_id"),
                "threats": doc.get("threats", []),
                "risk": doc.get("risk", 0)
            })
        return {"items": items}
    except Exception as e:
        logger.error(f"Error obteniendo amenazas: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo amenazas: {str(e)}")

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
