
# Si el pedido esta pago no se puede modificar

from enum import Enum
from .producto import Producto
from .cliente import Cliente

from .pago import Pago
from typing import List
from datetime import datetime

class Estado(Enum):
    PENDIENTE = 'Pendiente'
    EN_PROCESO = 'En Proceso'
    COMPLETADO = 'Completado'
    CANCELADO = 'Cancelado'

class Pedido:
    def __init__(self, cliente: Cliente, estado: Estado, valor_total: float,
                  pago: Pago):
        self.cliente = cliente
        self.estado = estado
        self.valor_total = valor_total
        self.pago = pago
        self.productos = []
        self.fecha_pedido = datetime.now()
    
    def __init__(self, cliente):
        self.cliente = cliente
        self.estado = Estado.EN_PROCESO
        self.pago = None
        self.productos = []
        self.valor_total = 0
        self.fecha_pedido = datetime.now()

    @classmethod
    def crearPedido(cls,cliente, productos: dict[Producto,int]):
        from .producto_unitario import ProductoUnitario
        p = Pedido(cliente)
        for pro in productos.keys():
            p.productos.append(ProductoUnitario(pro,p,productos[pro]))
            p.valor_total += pro.precio
        return p


    def agregarProductos(self, cliente, productos: dict[Producto,int]):
        from .producto_unitario import ProductoUnitario
        if not isinstance(cliente, Cliente):
            raise PermissionError("Solo un cliente puede agregar productos a un pedido")
        if cliente.cedula != self.cliente.cedula: 
             raise PermissionError("Solo el propetario puede agregar productos a un pedido")
        for pro in productos.keys():
            pu = ProductoUnitario(pro,productos[pro])
            pu.pedido = self
            self.productos.append(pu)
            self.valor_total += pro.precio*productos[pro]
            


            
        
