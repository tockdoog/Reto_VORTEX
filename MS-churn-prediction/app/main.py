# ======================================
# PUNTO DE ENTRADA DEL MICROSERVICIO
# ======================================
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection

# ======================================
# LIFESPAN - Eventos de Ciclo de Vida
# ======================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ========== STARTUP ==========
    print("🚀 Iniciando MS-Churn-Prediction-Service...")
    await connect_to_mongo()
    
    yield
    
    # ========== SHUTDOWN ==========
    print("🛑 Apagando servidor...")
    await close_mongo_connection()

# ======================================
# CREAR APLICACIÓN FASTAPI
# ======================================

app = FastAPI(
    title="MS-Churn-Prediction-Service",
    description="Microservicio de predicción de abandono de usuarios",
    version="1.0.0",
    lifespan=lifespan
)

# ======================================
# CONFIGURACIÓN DE CORS
# ======================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# INCLUIR ROUTERS
# ======================================

from app.api.v1.endpoints.prediction import router as churn_router

app.include_router(churn_router)

# ======================================
# RUTAS BÁSICAS
# ======================================

@app.get("/")
async def root():
    return {
        "message": "MS-Churn-Prediction-Service está corriendo",
        "status": "OK",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

# ======================================
# PUNTO DE EJECUCIÓN
# ======================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )
