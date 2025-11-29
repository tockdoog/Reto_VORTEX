from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

<<<<<<< HEAD
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
=======
class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto a analizar")
    ticket_id: Optional[str] = Field(None, description="ID del ticket asociado")
    language: str = Field("spanish", description="Idioma del texto")
    
    class Config:
        extra = "ignore"  # Ignora campos extraños en el JSON

class VectorizationResponse(BaseModel):
    vector: List[float] = Field(..., description="Vector de características")
    dimensions: int = Field(..., description="Dimensionalidad del vector")
    method: str = Field(..., description="Método de vectorización")
    features: Optional[List[str]] = Field(None, description="Nombres de características")

class SentimentResponse(BaseModel):
    sentiment: float = Field(..., description="Puntuación de sentimiento (-1 a 1)")
    label: str = Field(..., description="Etiqueta: negativo/neutral/positivo")
    confidence: float = Field(..., description="Confianza del análisis")
    positive_score: float = Field(..., description="Score positivo")
    negative_score: float = Field(..., description="Score negativo")

class TokenizationResponse(BaseModel):
    tokens: List[str] = Field(..., description="Lista de tokens")
    original_length: int = Field(..., description="Longitud del texto original")
    token_count: int = Field(..., description="Número de tokens")
    cleaned_text: str = Field(..., description="Texto después de limpieza")
    lemmas: Optional[List[str]] = Field(None, description="Lemas de los tokens")

class LinguisticFeatures(BaseModel):
    word_count: int
    sentence_count: int
    avg_word_length: float
    unique_words: int
    lexical_diversity: float
    readability_score: float
>>>>>>> Text-Analysis
