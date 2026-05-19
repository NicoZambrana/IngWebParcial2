import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde .env

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")