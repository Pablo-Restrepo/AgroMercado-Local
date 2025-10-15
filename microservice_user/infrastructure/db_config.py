import os
from dotenv import load_dotenv

# Ruta absoluta al .env en microservice_user
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

print("DATABASE_URL:", os.getenv("DATABASE_URL"))  # Depuración

# Configuración para SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
