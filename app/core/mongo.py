# ➡️ Conexión a MongoDB
# Se conecta a la base
# Crea colección predictions
# Función para guardar predicciones


from pymongo import MongoClient
from app.core.config import MONGO_URI

print("🔌 Intentando conectar a MongoDB en:", MONGO_URI)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Forzar conexión
    print("✅ Conectado correctamente a MongoDB")
except Exception as e:
    print("❌ Error conectando a MongoDB:", e)

db = client["classification_db"]
predictions_collection = db["predictions"]

def save_prediction(prediction: dict):
    print("📥 Guardando predicción en Mongo:", prediction)
    try:
        result = predictions_collection.insert_one(prediction)
        print("✅ Insertado con ID:", result.inserted_id)
    except Exception as e:
        print("❌ Error al insertar en MongoDB:", e)


