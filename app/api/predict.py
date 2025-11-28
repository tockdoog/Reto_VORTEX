# ➡️ La ruta que clasifica un ticket
# Recibe texto → responde clasificación (correctivo/evolutivo)
# Ahora es placeholder, luego usará el modelo real

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.model_loader import load_model_and_tokenizer, prepare_text
from app.core.mongo import save_prediction
import numpy as np

router = APIRouter()

class Ticket(BaseModel):
    text: str

@router.post("/predict")
def classify_ticket(ticket: Ticket):

    model, tokenizer = load_model_and_tokenizer()

    padded_text = prepare_text(ticket.text)

    prediction = float(model.predict(padded_text)[0][0])
    label = "evolutivo" if prediction >= 0.5 else "correctivo"

    result = {
        "label": label,
        "confidence": round(prediction, 4),
        "input_text": ticket.text
    }

    # save_prediction(result)

    return result

