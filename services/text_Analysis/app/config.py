import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://bootcamp:bootcamp1123@cluster0.aabjabq.mongodb.net/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "vortex_hackathon")
    TEXT_ANALYSIS_COLLECTION = os.getenv("TEXT_ANALYSIS_COLLECTION", "text_analysis_logs")
    SENTIMENT_MODEL_PATH = os.getenv("SENTIMENT_MODEL_PATH", "./models/sentiment_model.joblib")
    VECTORIZER_MODEL_PATH = os.getenv("VECTORIZER_MODEL_PATH", "./models/vectorizer.joblib")
    PORT = int(os.getenv("PORT", "4001"))
    SERVICE_HOST = os.getenv("TEXT_ANALYSIS_SERVICE_HOST", "http://localhost:4001")

settings = Settings()
