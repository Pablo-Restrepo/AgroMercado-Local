from app.models.producto import Producto
from app.models.pedido import Pedido

class ProductoUnitario:
    def __init__(self, producto: Producto, pedido: Pedido, cantidad: int):
        self.producto = producto
        self.pedido = pedido
        self.cantidad = cantidad