import os
from dotenv import load_dotenv

# Ruta absoluta al .env en microservice_user
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

print("DB_USER:", os.getenv("DB_USER"))  # Depuración

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}