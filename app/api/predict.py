# app/api/predict.py

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.core.model_loader import load_model_and_tokenizer, prepare_text
from app.core.mongo import save_prediction

router = APIRouter()

# ===============================
# Nuevo modelo de ticket oficial
# ===============================
class Ticket(BaseModel):
    ticket_id: str
    cliente: str
    proyecto: str
    fecha: str
    contacto_nombre: str
    contacto_correo: str
    contacto_telefono: str
    asunto: str
    descripcion: str


@router.post("/predict")
def classify_ticket(ticket: Ticket):

    # 1. Construir texto que analizará la IA
    texto_completo = f"{ticket.asunto}. {ticket.descripcion}"

    # 2. Cargar modelo
    model, tokenizer = load_model_and_tokenizer()
    padded_text = prepare_text(texto_completo)

    # 3. Predicción
    prediction = float(model.predict(padded_text)[0][0])
    label = "evolutivo" if prediction >= 0.5 else "correctivo"

    # 4. Resultado para guardar en MongoDB
    mongo_doc = {
        "ticket_id": ticket.ticket_id,
        "cliente": ticket.cliente,
        "proyecto": ticket.proyecto,
        "fecha": ticket.fecha,
        "contacto_nombre": ticket.contacto_nombre,
        "contacto_correo": ticket.contacto_correo,
        "contacto_telefono": ticket.contacto_telefono,
        "asunto": ticket.asunto,
        "descripcion": ticket.descripcion,
        "analizado_texto": texto_completo,
        "label": label,
        "confidence": round(prediction, 4),
        "timestamp": datetime.utcnow().isoformat()
    }

    print("➡️ Enviando documento a Mongo:", mongo_doc)

    # 5. Guardar en Mongo
    save_prediction(mongo_doc)

    # 6. Respuesta al cliente (limpia)
    return {
        "ticket_id": ticket.ticket_id,
        "label": label,
        "confidence": round(prediction, 4)
    }
