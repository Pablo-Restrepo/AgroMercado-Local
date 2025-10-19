from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from microservice_user.core.config import settings

engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    SQLModel.metadata.create_all(engine)
