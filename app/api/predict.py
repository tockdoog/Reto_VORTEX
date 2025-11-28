# ➡️ La ruta que clasifica un ticket
# Recibe texto → responde clasificación (correctivo/evolutivo)
# Ahora es placeholder, luego usará el modelo real

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Ticket(BaseModel):
    text: str

@router.post("/predict")
async def predict(ticket: Ticket):
    # Placeholder
    return {
        "classification": "pending_model",
        "confidence": 0.0,
        "received_text": ticket.text
    }
