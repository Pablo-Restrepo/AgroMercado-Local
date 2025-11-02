from .producto import Producto
from typing import List

class Cliente:
    def __init__(self, cedula: str, nombre: str, apellido: str, direccion: str):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion

    def crear_pedido(self, lista_productos: dict[Producto, int]):
        from .pedido import Pedido
        return Pedido.crearPedido(self,lista_productos)

    #def pagar_pedido():
    
    #def cosultar_pedido():
    
    #def consultar_pedidos():