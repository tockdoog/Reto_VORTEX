# =================================================================
# SERVICIO DE MACHINE LEARNING
# =================================================================

import random
from typing import Dict, Tuple, List
from datetime import datetime


class MLService:
    """
    Servicio que maneja toda la lógica de Machine Learning.
    """
    
    def __init__(self):
        """Constructor de la clase."""
        self.model = None
        self.model_info = None
        self.model_version = "v1.0_simple_rules"
        
        # Intentar cargar modelo entrenado
        try:
            import joblib
            import os
            
            model_path = "data/churn_model.pkl"
            info_path = "data/model_info.pkl"
            
            if os.path.exists(model_path) and os.path.exists(info_path):
                self.model = joblib.load(model_path)
                self.model_info = joblib.load(info_path)
                self.model_version = "v2.0_random_forest"
                print(f"✅ MLService inicializado con MODELO ENTRENADO (versión: {self.model_version})")
            else:
                print(f"⚠️  No se encontró modelo entrenado, usando reglas simples")
                print(f"✅ MLService inicializado (versión: {self.model_version})")
        except Exception as e:
            print(f"⚠️  Error cargando modelo: {e}")
            print(f"✅ MLService inicializado con reglas simples (versión: {self.model_version})")
    
    
    def predict_churn(
        self, 
        features: Dict
    ) -> Tuple[float, str, List[str]]:
        """Predice la probabilidad de churn."""
        
        if self.model is not None:
            return self._predict_with_model(features)
        else:
            return self._predict_with_rules(features)
    
    
    def _predict_with_model(
        self,
        features: Dict
    ) -> Tuple[float, str, List[str]]:
        """Predicción usando el modelo de ML entrenado."""
        
        import pandas as pd
        
        df = pd.DataFrame([features])
        feature_names = self.model_info['feature_names']
        
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0
        
        df = df[feature_names]
        
        churn_probability = self.model.predict_proba(df)[0][1]
        
        if churn_probability >= 0.7:
            risk_level = "HIGH"
        elif churn_probability >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        risk_factors = self._extract_risk_factors_ml(features, churn_probability)
        
        return (churn_probability, risk_level, risk_factors)
    
    
    def _predict_with_rules(
        self,
        features: Dict
    ) -> Tuple[float, str, List[str]]:
        """Predicción usando reglas simples (FALLBACK)."""
        
        churn_score = 0.0
        risk_factors = []
        
        tenure = features.get("tenure_months", 12)
        
        if tenure < 6:
            churn_score += 0.4
            risk_factors.append("Cliente nuevo (menos de 6 meses)")
        elif tenure < 12:
            churn_score += 0.2
            risk_factors.append("Cliente relativamente nuevo")
        
        num_tickets = features.get("num_tickets", 0)
        
        if num_tickets > 3:
            churn_score += 0.3
            risk_factors.append(f"{num_tickets} tickets abiertos (problemas frecuentes)")
        elif num_tickets > 1:
            churn_score += 0.15
            risk_factors.append("Algunos problemas detectados")
        
        sentiment = features.get("sentiment_score", 0.0)
        
        if sentiment < -0.3:
            churn_score += 0.3
            risk_factors.append("Sentimiento muy negativo detectado")
        elif sentiment < 0:
            churn_score += 0.15
            risk_factors.append("Sentimiento negativo")
        
        visits_last_month = features.get("visits_last_30_days", 10)
        
        if visits_last_month < 3:
            churn_score += 0.2
            risk_factors.append("Muy poca actividad reciente")
        
        churn_score = min(churn_score, 1.0)
        churn_score += random.uniform(-0.05, 0.05)
        churn_score = max(0.0, min(churn_score, 1.0))
        
        if churn_score >= 0.7:
            risk_level = "HIGH"
        elif churn_score >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return (churn_score, risk_level, risk_factors)
    
    
    def _extract_risk_factors_ml(
        self,
        features: Dict,
        churn_prob: float
    ) -> List[str]:
        """Extrae factores de riesgo basándose en las features."""
        factors = []
        
        tenure = features.get("tenure", features.get("tenure_months", 12))
        if tenure < 6:
            factors.append("Cliente nuevo (menos de 6 meses)")
        
        if features.get("Contract", "") == "Month-to-month":
            factors.append("Contrato mes a mes (sin compromiso)")
        
        monthly_charges = features.get("MonthlyCharges", features.get("monthly_charges", 0))
        if monthly_charges > 70:
            factors.append("Cargo mensual elevado")
        
        if churn_prob > 0.8:
            factors.append("Patrón de comportamiento de alto riesgo")
        
        if not factors:
            factors.append("Riesgo basado en análisis de patrones")
        
        return factors
    
    
    def generate_recommendation(
        self, 
        churn_probability: float,
        risk_level: str
    ) -> str:
        """Genera una recomendación basada en el riesgo."""
        
        if risk_level == "HIGH":
            return "Ofrecer descuento del 20% + soporte prioritario"
        elif risk_level == "MEDIUM":
            return "Enviar email personalizado con nuevas funcionalidades"
        else:
            return "Mantener comunicación regular"
    
    
    def should_show_exit_popup(self, churn_probability: float) -> bool:
        """Decide si el Dashboard debe mostrar el popup."""
        return churn_probability >= 0.7


# Creamos UNA SOLA instancia global
ml_service = MLService()
