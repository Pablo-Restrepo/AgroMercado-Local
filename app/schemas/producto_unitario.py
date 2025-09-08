from sqlmodel import SQLModel, Field,Relationship

from typing import Optional
from uuid import UUID, uuid4

class ProductoUnitarioBase(SQLModel):
    producto_id: UUID = Field(description="ID del producto")
    pedido_id: UUID = Field(description="ID del pedido")
    cantidad: int = Field(gt=0, description="Cantidad de productos en el pedido")

class ProductoUnitarioCreate(ProductoUnitarioBase):
    pass

class ProductoUnitarioRead(ProductoUnitarioBase):
    id: UUID

class ProductoUnitarioUpdate(SQLModel):
    producto_id: Optional[UUID] = None
    pedido_id: Optional[UUID] = None
    cantidad: Optional[int] = None

class ProductoUnitario(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    pedido_id: UUID = Field(foreign_key="pedido.id")
    producto_id: UUID = Field(foreign_key="producto.id")
    cantidad: int

    pedido: "Pedido" = Relationship(back_populates="productos_unitarios")
    producto: "Producto" = Relationship(back_populates="productos_unitarios")