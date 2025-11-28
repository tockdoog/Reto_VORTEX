from pymongo import MongoClient
from app.core.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["classification_db"]
predictions_collection = db["predictions"]

def save_prediction(prediction: dict):
    predictions_collection.insert_one(prediction)
