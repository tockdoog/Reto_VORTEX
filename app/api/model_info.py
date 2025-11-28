from fastapi import APIRouter

router = APIRouter()

@router.get("/model-info")
async def model_info():
    return {
        "model": "Not trained yet",
        "version": "1.0.0",
        "description": "Este microservicio clasificará tickets en Correctivo/Evolutivo"
    }
