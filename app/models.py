from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ClassificationRequest(BaseModel):
    text: Optional[str] = Field(None, description="Texto del ticket a clasificar")
    vector: Optional[List[float]] = Field(None, description="Vector de características del texto (opcional)")
    ticket_id: str = Field(..., description="ID del ticket")

class ClassificationResponse(BaseModel):
    prediction: str = Field(..., description="Tipo de mantenimiento: correctivo/evolutivo")
    confidence: float = Field(..., description="Confianza de la predicción (0-1)")
    ticket_id: str = Field(..., description="ID del ticket")
    model_version: str = Field(..., description="Versión del modelo utilizado")

class TrainingRequest(BaseModel):
    epochs: int = Field(10, description="Número de épocas de entrenamiento")
    validation_split: float = Field(0.2, description="Porcentaje de datos para validación")

class TrainingResponse(BaseModel):
    status: str = Field(..., description="Estado del entrenamiento")
    accuracy: float = Field(..., description="Precisión del modelo")
    loss: float = Field(..., description="Pérdida del modelo")
    training_time: float = Field(..., description="Tiempo de entrenamiento en segundos")

class ModelInfoResponse(BaseModel):
    model_version: str = Field(..., description="Versión del modelo")
    model_architecture: Dict[str, Any] = Field(..., description="Arquitectura del modelo")
    training_history: Dict[str, Any] = Field(..., description="Historial de entrenamiento")
    last_training: datetime = Field(..., description="Fecha del último entrenamiento")
    accuracy: float = Field(..., description="Precisión actual del modelo")