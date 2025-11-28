# ➡️ La ruta que entrena el modelo
# Endpoint POST que entrenará la IA


from fastapi import APIRouter

router = APIRouter()

@router.post("/train")
async def train_model():
    return {"status": "training_not_implemented_yet"}
