# =================================================================
# ENDPOINTS DE CHURN PREDICTION
# =================================================================
# Este archivo define las URLS (rutas) de tu API.
# Es donde el Dashboard u otros servicios llamarán.

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.churn import (
    PredictChurnRequest,
    PredictChurnResponse,
    ChurnStatusResponse,
    FeedbackRequest,
    FeedbackResponse,
    DailyChurnStatsResponse
)
from app.services.churn_service import churn_service

router = APIRouter(
    prefix="/api/churn",
    tags=["Churn Prediction"]
)
# prefix: Todas las rutas empezarán con /api/churn
# tags: Para agrupar en la documentación /docs


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 1: Predecir Churn
# ═══════════════════════════════════════════════════════════════

@router.post("/predict", response_model=PredictChurnResponse)
async def predict_churn(request: PredictChurnRequest):
    """
    Calcula la probabilidad de churn de un usuario.
    
    Este endpoint:
    1. Recibe datos del usuario (features)
    2. Calcula la probabilidad usando el ML Service
    3. Guarda el resultado en MongoDB
    4. Retorna la predicción
    
    URL FINAL: POST http://localhost:4003/api/churn/predict
    
    BODY (JSON):
    {
        "user_id": "USER_123",
        "features": {
            "tenure_months": 12,
            "num_tickets": 3,
            "sentiment_score": -0.4
        }
    }
    """
    
    # Llamar al servicio orquestador
    result = await churn_service.predict_churn(request)
    
    return result
    # FastAPI convierte automáticamente el objeto a JSON


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 2: Obtener Status (Para el Dashboard)
# ═══════════════════════════════════════════════════════════════

@router.get("/status/{user_id}", response_model=ChurnStatusResponse)
async def get_churn_status(user_id: str):
    """
    Obtiene el último status de churn de un usuario.
    
    Este es el endpoint MÁS IMPORTANTE para tu Dashboard.
    El frontend lo llamará cuando el usuario entre a la página.
    
    URL FINAL: GET http://localhost:4003/api/churn/status/USER_123
    
    RESPUESTA:
    {
        "user_id": "USER_123",
        "churn_probability": 0.85,
        "risk_level": "HIGH",
        "show_exit_popup": true,
        "popup_message": "¡Espera! Tenemos un descuento para ti"
    }
    
    El Dashboard puede usar 'show_exit_popup' para decidir
    si activar el listener de "exit intent".
    """
    
    # {user_id} en la URL se captura automáticamente
    # En Express sería: req.params.user_id
    
    result = await churn_service.get_churn_status(user_id)
    
    if not result:
        # Si no hay predicción, lanzar error 404
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró predicción para el usuario {user_id}"
        )
        # HTTPException es la forma de FastAPI de retornar errores HTTP
        # Equivalente en Express: res.status(404).json({...})
    
    return result


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 3: Registrar Feedback
# ═══════════════════════════════════════════════════════════════

@router.post("/feedback", response_model=FeedbackResponse)
async def register_feedback(request: FeedbackRequest):
    """
    Registra el feedback de una intervención.
    
    Cuando el Dashboard muestra una oferta al usuario
    y este la acepta/rechaza, llama a este endpoint.
    
    URL FINAL: POST http://localhost:4003/api/churn/feedback
    
    BODY:
    {
        "user_id": "USER_123",
        "intervention_type": "exit_popup_discount",
        "user_action": "accepted"
    }
    """
    
    result = await churn_service.register_feedback(request)
    
    return result


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 4: Estadísticas Diarias (Para el gráfico)
# ═══════════════════════════════════════════════════════════════

@router.get("/daily-stats", response_model=List[DailyChurnStatsResponse])
async def get_daily_stats(
    days: int = Query(default=30, ge=1, le=90)
):
    """
    Obtiene estadísticas diarias de churn.
    
    Este endpoint es para el GRÁFICO DE BARRAS del Dashboard:
    "Días vs Probabilidad de churn y Tickets"
    
    URL FINAL: GET http://localhost:4003/api/churn/daily-stats?days=30
    
    PARÁMETROS:
    - days: Cantidad de días a consultar (1-90, por defecto 30)
    
    RESPUESTA:
    [
        {
            "date": "2025-11-28",
            "avg_churn_probability": 0.62,
            "total_tickets": 15,
            "high_risk_users": 8
        },
        ...
    ]
    
    Tu Dashboard puede usar esto para graficar:
    - Eje X: date
    - Eje Y izquierdo: avg_churn_probability
    - Eje Y derecho: total_tickets
    """
    
    # Query() define parámetros de query string (?days=30)
    # ge=1 significa "greater or equal" (>= 1)
    # le=90 significa "less or equal" (<= 90)
    
    result = await churn_service.get_daily_stats(days)
    
    return result

