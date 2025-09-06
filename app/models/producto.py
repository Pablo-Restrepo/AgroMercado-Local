from uuid import UUID
from .base import SQLModel
from sqlmodel import Field, Relationship


class PedidoProductoLink(SQLModel, table=True):
    pedido_id: UUID = Field(
        foreign_key='pedido.id',
        primary_key=True
    )
    producto_id: UUID = Field(
        foreign_key='producto.id',
        primary_key=True
    )


class Producto(SQLModel, table=True):
    nombre: str
    precio: float
    cantidad: int

    pedidos: list['Pedido'] = Relationship(
        back_populates='productos',
        link_model=PedidoProductoLink
    )
