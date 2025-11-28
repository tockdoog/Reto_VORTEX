# Carga variables del .env
# Guarda MONGO_URI

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MODEL_PATH = "app/ml/classifier.h5"
TOKENIZER_PATH = "app/ml/tokenizer.pkl"
