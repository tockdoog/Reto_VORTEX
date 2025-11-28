# ➡️ La ruta que entrena el modelo
# Endpoint POST que entrenará la IA


from fastapi import APIRouter
from app.ml.trainer import train_model

router = APIRouter()

@router.post("/train")
def train():
    result = train_model()
    return result
