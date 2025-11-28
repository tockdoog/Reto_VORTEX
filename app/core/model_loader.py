# Modelo vacío por ahora (se implementará cuando entrenemos)
# Lee classifier.h5
# Lee tokenizer.pkl
# Luego será clave para /predict

import os
import pickle
from tensorflow.keras.models import load_model
from app.core.config import MODEL_PATH, TOKENIZER_PATH
from app.utils.preprocess import clean_text
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 100

model = None
tokenizer = None

def load_model_and_tokenizer():
    global model, tokenizer
    
    # Cargar modelo
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Modelo no encontrado. Entrena el modelo primero con /train")
        model = load_model(MODEL_PATH)

    # Cargar tokenizer
    if tokenizer is None:
        if not os.path.exists(TOKENIZER_PATH):
            raise FileNotFoundError("Tokenizer no encontrado. Entrena el modelo primero con /train")
        with open(TOKENIZER_PATH, "rb") as handle:
            tokenizer = pickle.load(handle)

    return model, tokenizer


def prepare_text(text: str):
    global tokenizer
    global model

    # Asegurar carga del modelo y tokenizer
    load_model_and_tokenizer()

    text_clean = clean_text(text)
    seq = tokenizer.texts_to_sequences([text_clean])
    padded = pad_sequences(seq, maxlen=MAX_LEN)
    return padded

