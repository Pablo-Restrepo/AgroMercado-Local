#Este archivo define los modelos ORM para la base de datos usando SQLAlchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class GremioORM(Base):
    __tablename__ = "Gremio"
    id = Column(String, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    creado_en = Column(DateTime, default=datetime.now(datetime.timezone.utc))

    productores = relationship("ProductorORM", back_populates="gremio")

class ProductorORM(Base):
    __tablename__ = "Productor"
    id = Column(String, primary_key=True)
    codigo = Column(String, nullable=False)
    persona_id = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="None")
    gremio_id = Column(String, ForeignKey("Gremio.id"), nullable=False)
    creado_en = Column(DateTime, default=datetime.now(datetime.timezone.utc))

    gremio = relationship("GremioORM", back_populates="productores")
