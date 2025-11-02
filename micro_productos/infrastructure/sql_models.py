from typing import Optional, List
from datetime import date, datetime
from sqlmodel import LargeBinary, SQLModel, Field, Relationship

class ProductorModel(SQLModel, table=True):
    __tablename__ = "productor"
    prod_id: int  = Field(default=None, primary_key=True)
    prod_nombre: str = Field(max_length=100)
    prod_apellido: str = Field(max_length=100)
    prod_cod_gremio: int = Field(default=None)
    prod_nombre_gremio: str = Field(max_length=100)

    
class ProductoModel(SQLModel, table=True):
    __tablename__ = "producto"
    p_id: int = Field(default=None, primary_key=True)
    p_nombre: str = Field(max_length=100)
    p_tipo:str = Field(max_length=100)
    p_unidad:str = Field(max_length=100)
    prod_id:int = Field(default=None, foreign_key="productor.prod_id")
    p_precio:float = Field(default=0)
    imagen: Optional[bytes] = Field(default=None, sa_type=LargeBinary(length=(2**24)))