
# Si el pedido esta pago no se puede modificar

from enum import Enum

from app.models.pago import Pago

class Estado(Enum):
    PENDIENTE = 'Pendiente'
    EN_PROCESO = 'En Proceso'
    COMPLETADO = 'Completado'
    CANCELADO = 'Cancelado'

class Pedido:
    def __init__(self, cliente, estado: Estado, valor_total: float, pago: Pago):
        self.cliente = cliente
        self.estado = estado
        self.valor_total = valor_total
        self.pago = pago