# app/api/predict.py

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

    # 1️ Cargar modelo y tokenizer
    model, tokenizer = load_model_and_tokenizer()

    # 2️ Preprocesar texto
    padded_text = prepare_text(ticket.text)

    # 3️ Hacer predicción
    prediction = float(model.predict(padded_text)[0][0])
    label = "evolutivo" if prediction >= 0.5 else "correctivo"

    # 4️ Resultado base
    result = {
        "label": label,
        "confidence": round(prediction, 4),
        "input_text": ticket.text
    }

    print("➡️ Enviando resultado a Mongo:", result)

    # 5️ Guardar en Mongo
    save_prediction(result)

    # crear una respuesta limpia sin `_id`
    response = {
        "label": result["label"],
        "confidence": result["confidence"],
        "input_text": result["input_text"]
    }

    return response
