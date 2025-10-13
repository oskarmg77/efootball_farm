import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env en la raíz del proyecto
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")