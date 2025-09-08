from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, List
from uuid import UUID, uuid4

class ProductoBase(SQLModel):
    id: UUID = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=50, description="Nombre del producto")
    precio: float = Field(description="Precio del producto")

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    pass

class ProductoUpdate(SQLModel):
    nombre: str | None = None
    precio: float

class Producto(SQLModel,table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    nombre: str = Field(min_length=2, max_length=50, description="Nombre del producto")
    precio: float = Field(description="Precio del producto")
    productos_unitarios: List["ProductoUnitario"] = Relationship(back_populates="producto")