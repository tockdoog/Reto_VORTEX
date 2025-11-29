# =================================================================
# SERVICIO ORQUESTADOR DE CHURN
# =================================================================
# Este archivo COORDINA todo el flujo de predicción de churn.
# Es el "manager" que usa el ML Service y guarda en MongoDB.

from datetime import datetime
from typing import Optional, List
from app.services.ml_service import ml_service
from app.db.mongodb import get_database
from app.models import ChurnPredictionModel, FeedbackModel
from app.schemas.churn import (
    PredictChurnRequest,
    PredictChurnResponse,
    ChurnStatusResponse,
    FeedbackRequest,
    FeedbackResponse,
    DailyChurnStatsResponse
)

# ══════════════════════════════════════════════════════════════
# 📚 CONCEPTO: Orquestador (Orchestrator)
# ══════════════════════════════════════════════════════════════
# Un orquestador es como el "director de orquesta".
# Coordina diferentes servicios para completar una tarea.
#
# Flujo típico:
# 1. Recibe datos del endpoint
# 2. Llama al ML Service para calcular
# 3. Guarda el resultado en MongoDB
# 4. Retorna la respuesta formateada
#
# Esto se conoce como "Separation of Concerns" (Separación de Responsabilidades)
# ══════════════════════════════════════════════════════════════


class ChurnService:
    """
    Servicio orquestador de Churn Prediction.
    
    Este servicio NO hace cálculos de ML directamente.
    Coordina entre el MLService y la base de datos.
    """
    
    def __init__(self):
        """Constructor vacío. La configuración ya está en otros lados."""
        pass
        # 'pass' en Python significa "no hacer nada"
        # Equivalente en TS: constructor() { }
    
    
    async def predict_churn(
        self, 
        request: PredictChurnRequest
    ) -> PredictChurnResponse:
        """
        Predice el churn de un usuario y guarda el resultado.
        
        FLUJO:
        1. Llamar al ML Service para calcular
        2. Guardar la predicción en MongoDB
        3. Retornar respuesta formateada
        """
        
        # ════════════════════════════════════════════════════
        # PASO 1: Calcular probabilidad con el ML Service
        # ════════════════════════════════════════════════════
        churn_prob, risk_level, risk_factors = ml_service.predict_churn(
            request.features
        )
        # Esto DESEMPAQUETA la tupla en 3 variables separadas
        # En JS sería: const [prob, level, factors] = predict(...);
        
        # ════════════════════════════════════════════════════
        # PASO 2: Generar recomendación
        # ════════════════════════════════════════════════════
        recommendation = ml_service.generate_recommendation(
            churn_prob,
            risk_level
        )
        
        # ════════════════════════════════════════════════════
        # PASO 3: Guardar en MongoDB
        # ════════════════════════════════════════════════════
        db = get_database()
        collection = db["churn_predictions"]
        # En MongoDB, una "collection" es como una tabla SQL
        # Equivalente en SQL: SELECT * FROM churn_predictions
        
        prediction_doc = {
            "user_id": request.user_id,
            "churn_probability": churn_prob,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "features_used": request.features,
            "model_version": ml_service.model_version,
            "created_at": datetime.utcnow()
        }
        
        # insert_one() guarda UN documento en MongoDB
        # 'await' espera a que termine de guardar
        await collection.insert_one(prediction_doc)
        
        # ════════════════════════════════════════════════════
        # PASO 4: Retornar respuesta
        # ════════════════════════════════════════════════════
        return PredictChurnResponse(
            user_id=request.user_id,
            churn_probability=churn_prob,
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendation=recommendation,
            timestamp=datetime.utcnow()
        )
        # Esto crea una instancia del schema PredictChurnResponse
        # Pydantic validará automáticamente que todo sea correcto
    
    
    async def get_churn_status(
        self, 
        user_id: str
    ) -> Optional[ChurnStatusResponse]:
        """
        Obtiene el último status de churn de un usuario.
        
        Este es el endpoint que el Dashboard llamará para saber
        si debe mostrar el popup de "¡No te vayas!"
        
        RETORNA:
        - ChurnStatusResponse si encuentra datos
        - None si el usuario no tiene predicciones
        """
        
        db = get_database()
        collection = db["churn_predictions"]
        
        # Buscar la predicción MÁS RECIENTE de este usuario
        prediction = await collection.find_one(
            {"user_id": user_id},  # Filtro: WHERE user_id = ...
            sort=[("created_at", -1)]  # Ordenar por fecha DESC
        )
        # find_one() retorna UN solo documento (o None)
        # -1 significa DESCENDENTE (más reciente primero)
        # 1 sería ASCENDENTE (más antiguo primero)
        
        if not prediction:
            return None
            # Si no hay predicción, retornar None (null en JS)
        
        # Si sí hay, formatear la respuesta
        show_popup = ml_service.should_show_exit_popup(
            prediction["churn_probability"]
        )
        
        popup_message = None
        if show_popup:
            popup_message = "¡Espera! Tenemos un 20% de descuento para ti 🎁"
        
        return ChurnStatusResponse(
            user_id=user_id,
            churn_probability=prediction["churn_probability"],
            risk_level=prediction["risk_level"],
            last_updated=prediction["created_at"],
            show_exit_popup=show_popup,
            popup_message=popup_message
        )
    
    
    async def register_feedback(
        self, 
        request: FeedbackRequest
    ) -> FeedbackResponse:
        """
        Registra el feedback de una intervención.
        
        Cuando el usuario acepta/rechaza una oferta en el Dashboard,
        guardamos esa información para mejorar el modelo en el futuro.
        """
        
        # ════════════════════════════════════════════════════
        # Buscar la última predicción para saber el score
        # ════════════════════════════════════════════════════
        db = get_database()
        predictions_coll = db["churn_predictions"]
        
        last_prediction = await predictions_coll.find_one(
            {"user_id": request.user_id},
            sort=[("created_at", -1)]
        )
        
        churn_prob = last_prediction["churn_probability"] if last_prediction else 0.0
        
        # ════════════════════════════════════════════════════
        # Guardar el feedback
        # ════════════════════════════════════════════════════
        feedback_coll = db["feedback"]
        
        feedback_doc = {
            "user_id": request.user_id,
            "prediction_churn_prob": churn_prob,
            "intervention_type": request.intervention_type,
            "user_action": request.user_action,
            "timestamp": datetime.utcnow()
        }
        
        await feedback_coll.insert_one(feedback_doc)
        
        return FeedbackResponse(
            message="Feedback registrado exitosamente",
            user_id=request.user_id,
            saved_at=datetime.utcnow()
        )
    
    
    async def get_daily_stats(
        self, 
        days: int = 30
    ) -> List[DailyChurnStatsResponse]:
        """
        Obtiene estadísticas diarias de churn.
        
        Este endpoint es para el gráfico de barras del Dashboard:
        "Días vs Probabilidad de churn y Tickets"
        
        PARÁMETROS:
        - days: Cuántos días hacia atrás consultar (por defecto 30)
        
        RETORNA:
        Lista de estadísticas por día.
        """
        
        # TODO: Implementar agregaciones de MongoDB
        # Por ahora retornamos datos dummy para que el Dashboard funcione
        
        from datetime import timedelta
        
        stats = []
        today = datetime.utcnow()
        
        for i in range(days):
            date = today - timedelta(days=i)
            
            # Generar datos aleatorios realistas
            import random
            stats.append(
                DailyChurnStatsResponse(
                    date=date.strftime("%Y-%m-%d"),
                    avg_churn_probability=round(random.uniform(0.4, 0.8), 2),
                    total_tickets=random.randint(5, 25),
                    high_risk_users=random.randint(2, 15)
                )
            )
        
        return stats


# ══════════════════════════════════════════════════════════════
# Crear instancia global del orquestador
# ══════════════════════════════════════════════════════════════
churn_service = ChurnService()
