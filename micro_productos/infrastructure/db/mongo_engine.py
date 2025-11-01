from mongoengine import connect, disconnect
from core.config import Settings


# URL de conexión a MongoDB (por ejemplo: "mongodb://usuario:password@localhost:27017/mi_base")
MONGO_DATABASE_URL = Settings.MONGO_DATABASE_URL


def init_mongo_db():
    """
    Inicializa la conexión con MongoDB usando MongoEngine.
    Debe llamarse al iniciar la aplicación.
    """
    connect(host=MONGO_DATABASE_URL)


def close_mongo_db():
    """
    Cierra la conexión con MongoDB (opcional, útil para tests o apagado limpio).
    """
    disconnect()
