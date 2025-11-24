from typing import Optional
from sqlmodel import LargeBinary, SQLModel, Field, Relationship
from sqlalchemy import CheckConstraint

class ProductorModel(SQLModel, table=True):
    __tablename__ = "productor"
    prod_id: int  = Field(default=None, primary_key=True)
    prod_nombre: str = Field(max_length=100)
    prod_apellido: str = Field(max_length=100)
    prod_cod_gremio: int = Field(default=None)
    prod_nombre_gremio: str = Field(max_length=100)

    
class ProductoModel(SQLModel, table=True):
    __tablename__ = "producto"

    __table_args__ = (
        CheckConstraint("p_precio > 0", name="check_p_precio_mayor_cero"),
        CheckConstraint("p_stock > 0", name="check_p_stock_mayor_cero"),
    )
    p_id: int = Field(default=None, primary_key=True)
    p_nombre: str = Field(max_length=100)
    p_tipo:str = Field(max_length=100)
    p_unidad:str = Field(max_length=100)
    prod_id:int = Field(default=None, foreign_key="productor.prod_id")
    p_precio:float = Field(default=0)
    p_stock: int  = Field(default=0)
    p_estado: bool = Field(default=True)
    imagen: Optional[bytes] = Field(default=None, sa_type=LargeBinary(length=(2**24)))