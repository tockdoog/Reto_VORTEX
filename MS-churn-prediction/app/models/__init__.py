# =================================================================
# MODELOS DE DATOS - MONGODB
# =================================================================
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class ChurnPredictionModel(BaseModel):
    # ════ CAMPOS OBLIGATORIOS ════

    user_id: str = Field(..., description="ID único del usuario")
    # El "..." significa "campo obligatorio" (como required en TS)
    # Field() permite agregar metadatos (descripción, validaciones, etc.)
    
    churn_probability: float = Field(
        ..., 
        ge=0.0,  # ge = "greater or equal" (mayor o igual a 0)
        le=1.0,  # le = "less or equal" (menor o igual a 1)
        description="Probabilidad de churn (0.0 a 1.0)"
    )
    
    risk_level: str = Field(
        ...,
        description="Nivel de riesgo: LOW, MEDIUM, HIGH"
    )
    
    # ════ CAMPOS OPCIONALES ════
    
    risk_factors: Optional[List[str]] = Field(
        default=[],  # Valor por defecto: lista vacía
        description="Lista de factores que aumentan el riesgo"
    )
    # Optional[List[str]] = string[] | null en TypeScript
    
    features_used: Optional[Dict] = Field(
        default={},
        description="Features del usuario usadas en la predicción"
    )
    # Dict = { [key: string]: any } en TypeScript
    
    model_version: str = Field(
        default="v1.0",
        description="Versión del modelo usado"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha de creación"
    )
    # default_factory es una función que se ejecuta
    # cada vez que creates un objeto nuevo
    # (como () => new Date() en TS)
    
    # ════ CONFIGURACIÓN ════
    
    class Config:
        """
        Configuración del modelo Pydantic.
        
        Esta clase interna le dice a Pydantic cómo comportarse.
        """
        # Permitir guardar como diccionario Python
        json_schema_extra = {
            "example": {
                "user_id": "USER_12345",
                "churn_probability": 0.85,
                "risk_level": "HIGH",
                "risk_factors": ["Bajo uso", "Sin compras"],
                "model_version": "v1.0"
            }
        }


class FeedbackModel(BaseModel):
    """
    Modelo de Feedback del usuario.
    
    Cuando el Dashboard muestra una oferta al usuario
    y este la acepta/rechaza, guardamos ese feedback aquí.
    
    Esto sirve para mejorar el modelo en el futuro.
    """
    
    user_id: str = Field(..., description="ID del usuario")
    
    prediction_churn_prob: float = Field(
        ...,
        description="Qué probabilidad tenía cuando se mostró la oferta"
    )
    
    intervention_type: str = Field(
        ...,
        description="Tipo de intervención: 'exit_popup', 'email', etc."
    )
    
    user_action: str = Field(
        ...,
        description="Acción del usuario: 'accepted', 'rejected', 'ignored'"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Cuándo ocurrió"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "USER_12345",
                "prediction_churn_prob": 0.85,
                "intervention_type": "exit_popup_discount",
                "user_action": "accepted",
            }
        }