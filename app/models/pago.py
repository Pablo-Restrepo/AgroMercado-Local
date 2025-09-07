from enum import Enum
from .base import SQLModel
from sqlmodel import Relationship


class MetodoPago(Enum):
    NEQUI = 'Nequi'
    PAYPAL = 'Paypal'
    TARJETA = 'Tarjeta'
    EFECTIVO = 'Efectivo'


class Pago():
    def __init__(self, metodo: MetodoPago, idPedido: str):
        self.metodo = metodo
        self.idPedido = idPedido
