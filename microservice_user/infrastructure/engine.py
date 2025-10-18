from sqlmodel import create_engine, Session, SQLModel
from microservice_user.infrastructure.db_config import db_config

def get_database_url() -> str:
    user = db_config.get("user")
    password = db_config.get("password")
    host = db_config.get("host") or "localhost"
    database = db_config.get("database")
    return f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    # Crear tablas si no existen
    from microservice_user.infrastructure.models import PersonaModel, UsuarioModel
    SQLModel.metadata.create_all(engine)