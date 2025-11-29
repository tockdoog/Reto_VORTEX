import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PORT = int(os.getenv("PORT", "5005"))

settings = Settings()
