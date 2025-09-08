from .producto import Producto
from .pedido import Pedido

class ProductoUnitario:
    def __init__(self, producto: Producto,pedido: Pedido, cantidad: int):
        self.producto = producto
        self.pedido = pedido
        self.cantidad = cantidad