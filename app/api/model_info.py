# ➡️ La ruta que dice qué modelo está usando la API
# Devuelve información estática del modelo
# Es documentación interna (versión, descripción)

from fastapi import APIRouter

router = APIRouter()

@router.get("/model-info")
async def model_info():
    return {
        "model": "Not trained yet",
        "version": "1.0.0",
        "description": "Este microservicio clasificará tickets en Correctivo/Evolutivo"
    }

