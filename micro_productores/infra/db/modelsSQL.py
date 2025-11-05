from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class GremioModel(SQLModel, table=True):
    __tablename__ = "gremio"  # Define explícitamente el nombre de la tabla

    gre_id: Optional[int] = Field(default=None, primary_key=True)
    gre_nombre: str = Field(max_length=100)
    gre_fecha_creacion: datetime = Field(default_factory=datetime.now)

    # Relación con productores
    productores: List["ProductorModel"] = Relationship(back_populates="gremio")


class ProductorModel(SQLModel, table=True):
    __tablename__ = "productor"  # Define explícitamente el nombre de la tabla
    prod_id: Optional[int] = Field(default=None, primary_key=True)
    prod_codigo: str = Field(nullable=True,default=None, max_length=50, unique=True)
    prod_nombres: str = Field(max_length=100)
    prod_apellidos: str = Field(max_length=100)
    prod_es_activo: bool = Field(default=True)
    gre_id: Optional[int] = Field(nullable=True, default=None, foreign_key="gremio.gre_id")
    prod_rol: str = Field(max_length=50)
    prod_fecha_creacion: datetime = Field(default_factory=datetime.now)
    u_id:int = Field(nullable=False,unique=True)
    # Relación con gremio
    gremio: Optional[GremioModel] = Relationship(back_populates="productores")        