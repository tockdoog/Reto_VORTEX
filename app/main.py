# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import mongodb
from app.models import ClassificationRequest, ClassificationResponse, TrainingRequest, TrainingResponse, ModelInfoResponse
from app.services.classification_model import ClassificationModel
from app.services.data_processor import DataProcessor
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MS-Classification-Service", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar el modelo y procesador de datos
classification_model = ClassificationModel()
data_processor = DataProcessor()

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 MS-Classification-Service iniciado")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 MS-Classification-Service detenido")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "MS-Classification-Service", "timestamp": datetime.now()}

@app.post("/api/classification/predict", response_model=ClassificationResponse)
async def predict(request: ClassificationRequest):
    try:
        # Si se proporciona texto, debemos convertirlo a vector (aquí asumimos que ya tenemos el vector)
        # En un caso real, llamaríamos al MS-Text-Analysis para obtener el vector
        if request.text and not request.vector:
            # Por ahora, generamos un vector aleatorio para simular
            # En producción, aquí se haría una petición al MS-Text-Analysis
            vector = [0.1] * 1000
        elif request.vector:
            vector = request.vector
        else:
            raise HTTPException(status_code=400, detail="Se debe proporcionar texto o vector")

        # Realizar predicción
        result = classification_model.predict(vector)
        
        # Guardar en base de datos
        collection = mongodb.get_collection("classification_logs")
        log_entry = {
            "ticket_id": request.ticket_id,
            "text": request.text,
            "vector_length": len(vector),
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "model_version": classification_model.model_version,
            "timestamp": datetime.now()
        }
        collection.insert_one(log_entry)

        return ClassificationResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            ticket_id=request.ticket_id,
            model_version=classification_model.model_version
        )
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.post("/api/classification/train", response_model=TrainingResponse)
async def train(request: TrainingRequest):
    try:
        # Cargar datos de entrenamiento
        df = data_processor.load_training_data("data/training_data.csv")
        X, y = data_processor.prepare_data(df)
        
        # Entrenar el modelo
        start_time = datetime.now()
        history = classification_model.train(X, y, epochs=request.epochs, validation_split=request.validation_split)
        training_time = (datetime.now() - start_time).total_seconds()
        
        # Calcular métricas
        accuracy = history.history['accuracy'][-1]
        loss = history.history['loss'][-1]
        
        return TrainingResponse(
            status="entrenamiento completado",
            accuracy=accuracy,
            loss=loss,
            training_time=training_time
        )
    except Exception as e:
        logger.error(f"Error en entrenamiento: {e}")
        raise HTTPException(status_code=500, detail=f"Error en entrenamiento: {str(e)}")

@app.get("/api/classification/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """Endpoint para obtener información del modelo"""
    try:
        model_info = classification_model.get_model_info()
        
        if not model_info:
            raise HTTPException(status_code=404, detail="Modelo no disponible")
        
        return ModelInfoResponse(
            model_version=model_info["model_version"],
            model_architecture={
                "layers": model_info.get("layers", 0),
                "trainable_parameters": model_info.get("input_features", 0),
                "model_type": model_info.get("model_type", "Unknown")
            },
            training_history=classification_model.training_history,
            last_training=datetime.now(),
            accuracy=classification_model.training_history.get('accuracy', [0.5])[-1] if classification_model.training_history else 0.5
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo información del modelo: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo información del modelo: {str(e)}")