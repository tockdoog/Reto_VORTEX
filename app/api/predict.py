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
