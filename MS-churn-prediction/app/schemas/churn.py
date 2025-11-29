# =================================================================
# SCHEMAS - VALIDACIÓN DE REQUESTS Y RESPONSES
# =================================================================
# Este archivo define cómo deben verse los datos que ENTRAN y SALEN
# de tus endpoints (tu API).
#
# Diferencia con models.py:
# - models.py   → Cómo se GUARDAN en la base de datos
# - schemas.py  → Cómo se ENVÍAN/RECIBEN por la API
#
# A veces son iguales, pero separarlos es buena práctica.

from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# 📚 LECCIÓN DE PYTHON #3: Request vs Response
# ══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# REQUEST SCHEMAS (Lo que el cliente ENVÍA)
# ═══════════════════════════════════════════════════════════════

class PredictChurnRequest(BaseModel):
    """
    Schema para el endpoint POST /api/churn/predict
    
    Esto es lo que el Dashboard (u otro servicio) te enviará
    para que calcules la probabilidad de churn.
    """
    
    user_id: str = Field(
        ...,
        description="ID único del usuario",
        example="USER_12345"
    )
    
    # ════ Features del usuario (características) ════
    # Optional significa que si no envían el campo, no pasa nada
    features: Dict = Field(
        default={},
        description="Características del usuario para predecir churn",
        example={
            "tenure_months": 12,
            "monthly_charges": 65.5,
            "total_charges": 786.0,
            "num_tickets": 3,
            "sentiment_score": -0.4
        }
    )


class FeedbackRequest(BaseModel):
    """
    Schema para el endpoint POST /api/churn/feedback
    
    Cuando el usuario interactúa con una oferta en el Dashboard,
    este envía feedback para que aprendamos qué funciona.
    """
    
    user_id: str = Field(..., description="ID del usuario")
    
    intervention_type: str = Field(
        ...,
        description="Tipo de oferta mostrada",
        example="exit_popup_discount"
    )
    
    user_action: str = Field(
        ...,
        description="Qué hizo el usuario",
        example="accepted"  # o "rejected", "ignored"
    )


# ═══════════════════════════════════════════════════════════════
# RESPONSE SCHEMAS (Lo que tu API RETORNA)
# ═══════════════════════════════════════════════════════════════

class PredictChurnResponse(BaseModel):
    """
    Schema de respuesta para POST /api/churn/predict
    
    Esto es lo que retornas después de calcular el churn.
    El Dashboard lo usará para mostrar gráficos.
    """
    
    user_id: str
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    risk_factors: List[str] = []
    recommendation: Optional[str] = None
    timestamp: datetime
    
    class Config:
        # Ejemplo que aparecerá en la documentación /docs
        json_schema_extra = {
            "example": {
                "user_id": "USER_12345",
                "churn_probability": 0.85,
                "risk_level": "HIGH",
                "risk_factors": [
                    "Bajo uso últimos 30 días",
                    "Sentimiento negativo"
                ],
                "recommendation": "Ofrecer descuento del 20%",
                "timestamp": "2025-11-28T21:00:00Z"
            }
        }


class ChurnStatusResponse(BaseModel):
    """
    Schema de respuesta para GET /api/churn/status/{user_id}
    
    Este endpoint es el que el Dashboard llamará para saber
    si debe mostrar el popup de "¡No te vayas!"
    
    Es MÁS SIMPLE que el de predicción porque ya calculaste
    el riesgo antes. Solo retornas lo guardado en MongoDB.
    """
    
    user_id: str
    churn_probability: float
    risk_level: str
    last_updated: datetime
    show_exit_popup: bool  # True si riesgo > 70%
    popup_message: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "USER_12345",
                "churn_probability": 0.85,
                "risk_level": "HIGH",
                "last_updated": "2025-11-28T20:00:00Z",
                "show_exit_popup": True,
                "popup_message": "¡Espera! Tenemos un 20% de descuento"
            }
        }


class FeedbackResponse(BaseModel):
    """
    Respuesta simple cuando se registra feedback.
    """
    
    message: str = "Feedback registrado exitosamente"
    user_id: str
    saved_at: datetime


class DailyChurnStatsResponse(BaseModel):
    """
    NUEVO: Endpoint para el gráfico de barras del Dashboard.
    
    El Dashboard muestra:
    "Días vs Probabilidad de churn y Tickets recibidos"
    
    Este schema le da los datos en el formato que necesita.
    """
    
    date: str = Field(..., description="Fecha (YYYY-MM-DD)")
    avg_churn_probability: float = Field(
        ...,
        description="Promedio de churn ese día"
    )
    total_tickets: int = Field(
        ...,
        description="Cantidad de tickets ese día"
    )
    high_risk_users: int = Field(
        ...,
        description="Usuarios con riesgo alto ese día"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-11-28",
                "avg_churn_probability": 0.62,
                "total_tickets": 15,
                "high_risk_users": 8
            }
        }