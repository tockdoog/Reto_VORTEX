from pymongo import MongoClient
from app.config import settings
import logging

class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.database = self.client[settings.DATABASE_NAME]
            logging.info("✅ Conectado a MongoDB exitosamente - Classification Service")
        except Exception as e:
            logging.error(f"❌ Error conectando a MongoDB: {e}")

    def get_collection(self, collection_name):
        return self.database[collection_name]

# Instancia global
mongodb = MongoDB()