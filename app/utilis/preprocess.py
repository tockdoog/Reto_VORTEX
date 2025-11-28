import re

def clean_text(text: str):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9áéíóúñ ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
