# ======================================
# CONFIGURACIÓN GLOBAL DEL PROYECTO
# ======================================

# En Pydantic v2, BaseSettings se movió a un paquete separado
from pydantic_settings import BaseSettings

# BaseSettings es una clase especial que automáticamente
# lee el archivo .env y valida los datos
class Settings(BaseSettings):
    # Puerto del servidor (por defecto 4003)
    PORT: int = 4003
    
    # URL de conexión a MongoDB Atlas
    MONGODB_URL: str
    
    # Nombre de la base de datos
    DATABASE_NAME: str = "churn_prediction_db"
    
    # Ruta al modelo entrenado
    MODEL_PATH: str = "./data/churn_model.pkl"
    
    class Config:
        # Le dice a Pydantic que busque el archivo .env
        env_file = ".env"
        # Permitir campos extra que no estén definidos
        extra = "allow"

# Creamos UNA instancia global de la configuración
# Esto es como hacer: export const settings = loadEnv();
settings = Settings()
