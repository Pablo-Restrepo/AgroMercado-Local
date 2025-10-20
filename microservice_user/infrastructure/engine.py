from sqlmodel import create_engine, SQLModel
from microservice_user.infrastructure.db_config import db_config


def get_database_url() -> str:
    user = db_config.get("user")
    password = db_config.get("password")
    host = db_config.get("host", "localhost")
    database = db_config.get("database")
    return f"mysql+pymysql://{user}:{password}@{host}/{database}"


DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    # Importar los modelos antes de crear las tablas
    from microservice_user.infrastructure.modelsSQL import PersonaModel, UsuarioModel

    # Crear todas las tablas
    SQLModel.metadata.create_all(engine)
