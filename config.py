import os
from dotenv import load_dotenv
load_dotenv()

# Variables de entorno cargadas desde .env
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Umbral de reconocimiento
RECOGNITION_THRESHOLD = 14.0