from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto a analizar")
    ticket_id: Optional[str] = Field(None, description="ID del ticket asociado")
    language: str = Field("spanish", description="Idioma del texto")
    class Config:
        extra = "ignore"

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

class SecurityResponse(BaseModel):
    isSafe: bool
    threatsDetected: List[str]
    anonymizedText: str
