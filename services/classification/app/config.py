import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://bootcamp:bootcamp1123@cluster0.aabjabq.mongodb.net/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "vortex_hackathon")
    CLASSIFICATION_COLLECTION = os.getenv("CLASSIFICATION_COLLECTION", "classification_logs")
    MODEL_PATH = os.getenv("MODEL_PATH", "./models/classification_model.h5")
    TRAINING_DATA_PATH = os.getenv("TRAINING_DATA_PATH", "./data/training_data.csv")
    PORT = int(os.getenv("PORT", "4002"))
    TEXT_ANALYSIS_SERVICE_URL = os.getenv("TEXT_ANALYSIS_SERVICE_URL", "http://localhost:4001")

settings = Settings()