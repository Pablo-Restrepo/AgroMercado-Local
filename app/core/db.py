from sqlmodel import SQLModel, create_engine
from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URL))


def init_db():
    SQLModel.metadata.create_all(engine)
