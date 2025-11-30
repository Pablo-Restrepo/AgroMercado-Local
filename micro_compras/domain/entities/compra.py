"""Clase que representa una compra en el sistema de micro compras."""
from datetime import datetime
from domain.entities.producto_unitario import ProductoUnitario
from domain.entities.estado_compra import *

class Compra:
    def __init__(self, id_usuario: int, productos: list[ProductoUnitario] ,id: int=None, fecha: datetime = datetime.now(), total: float = None, estado: EstadoCompra=EstadoCreada()):
        if id_usuario is None:
            raise ValueError("Todos los campos son obligatorios.")
        self.id = id
        self.id_usuario = id_usuario
        self.productos = productos
        self.fecha = fecha        
        self.total = total
        self.estado = estado
    def calcular_total(self)->float:
        if self.productos is None or len(self.productos) == 0:
            return 0        
        self.total = sum([producto.subtotal for producto in self.productos])
        return self.total    
    def agregar_producto(self, producto: ProductoUnitario):
        if self.estado == EstadoConfirmada() or self.estado == EstadoCancelada():
            raise ValueError("No se pueden agregar productos a una compra confirmada o cancelada.")
        #Si ya existe el producto en la lista, se actualiza la cantidad
        for p in self.productos:
            if p.id_producto == producto.id_producto:
                p.cantidad += producto.cantidad
                p.calcular_subtotal()
                return
        #Si no existe, se agrega a la lista
        self.productos.append(producto)
        self.calcular_total()        
    def eliminar_producto(self, id_producto: int):
        """Elimina un producto de la compra por su ID."""
        # Verificar si la compra está en un estado que permite eliminar productos
        if self.estado == EstadoConfirmada() or self.estado == EstadoCancelada():
            raise ValueError("No se pueden eliminar productos de una compra confirmada o cancelada.")
        self.productos = [p for p in self.productos if p.id_producto != id_producto]
        self.calcular_total()
        if len(self.productos) == 0:
            self.estado = EstadoCreada()        
    def vaciar_compra(self):
        self.productos = []
        self.total = 0
        self.estado = EstadoCreada()
    def confirmar_compra(self):
        if len(self.productos) == 0:
            raise ValueError("No se puede confirmar una compra vacía.")
        self.estado.confirmar(self)
    def pagar_compra(self):
        self.estado.pagar(self)
    def enviar_compra(self):
        self.estado.enviar(self)
    def cancelar_compra(self):
        self.estado.cancelar(self)
    def to_dict(self)-> dict:
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "productos": [producto.to_dict() for producto in self.productos],
            "fecha": self.fecha.isoformat(),
            "total": self.total,
            "estado": self.estado.nombre
        }