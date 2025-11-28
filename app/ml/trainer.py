import pandas as pd
import numpy as np
import pickle
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from app.utils.preprocess import clean_text

MODEL_PATH = "app/ml/classifier.h5"
TOKENIZER_PATH = "app/ml/tokenizer.pkl"
MAX_WORDS = 5000
MAX_LEN = 100

def train_model():
    # 1. Cargar dataset
    df = pd.read_csv("app/ml/dataset.csv")

    df["text"] = df["text"].astype(str).apply(clean_text)
    texts = df["text"].values
    labels = df["label"].values

    # 2. Tokenizer
    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_LEN)

    # 3. Modelo
    model = Sequential([
        Embedding(MAX_WORDS, 64, input_length=MAX_LEN),
        LSTM(64, return_sequences=False),
        Dropout(0.3),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid")
    ])

    model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )

    # 4. Entrenamiento
    callback = EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)

    history = model.fit(
        padded_sequences, labels,
        epochs=15,
        batch_size=16,
        validation_split=0.2,
        callbacks=[callback],
        verbose=1
    )

    # 5. Guardar modelo
    model.save(MODEL_PATH)

    # 6. Guardar tokenizer
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f)

    # 7. Retornar métricas para el endpoint
    return {
        "message": "Modelo entrenado correctamente",
        "loss": history.history["loss"],
        "accuracy": history.history["accuracy"],
    }
