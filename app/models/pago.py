from enum import Enum
from .base import SQLModel
from sqlmodel import Relationship


class MetodoPago(Enum):
    NEQUI = 'Nequi'
    PAYPAL = 'Paypal'
    TARJETA = 'Tarjeta'
    EFECTIVO = 'Efectivo'


class Pago(SQLModel, table=True):
    metodo: MetodoPago

    pedido: 'Pedido' = Relationship(back_populates='pago')
