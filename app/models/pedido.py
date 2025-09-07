from uuid import UUID
from enum import Enum
from .base import SQLModel
from .producto import PedidoProductoLink
from sqlmodel import Field, Relationship


class Estado(Enum):
    PENDIENTE = 'Pendiente'
    EN_PROCESO = 'En Proceso'
    COMPLETADO = 'Completado'
    CANCELADO = 'Cancelado'


class Pedido(SQLModel, table=True):
    estado: Estado = Estado.PENDIENTE
    valor_total: float

    cliente_id: UUID = Field(foreign_key='cliente.id')
    cliente: 'Cliente' = Relationship(back_populates='pedidos')

    productos: list['Producto'] = Relationship(
        back_populates='pedidos',
        link_model=PedidoProductoLink
    )

    pago_id: UUID = Field(foreign_key='pago.id')
    pago: 'Pago' = Relationship(back_populates='pedido')


# Si el pedido esta pago no se puede modificar