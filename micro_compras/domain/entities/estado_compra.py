from abc import ABC, abstractmethod
from enum import Enum

class EstadoCompraEnum(str, Enum):
    CREADA = "CREADA"
    CONFIRMADA = "CONFIRMADA"
    PAGADA = "PAGADA"
    ENVIADA = "ENVIADA"
    CANCELADA = "CANCELADA"
class EstadoCompra(ABC):
    @abstractmethod
    def confirmar(self, compra): ...
    @abstractmethod
    def pagar(self, compra): ...
    @abstractmethod
    def enviar(self, compra): ...
    @abstractmethod
    def cancelar(self, compra): ...
 
class EstadoCreada(EstadoCompra):
    def __init__(self):
        self.nombre = EstadoCompraEnum.CREADA
    def confirmar(self, compra):
        compra.estado = EstadoConfirmada()
        print("Compra confirmada.")
    
    def pagar(self, compra):
        raise Exception("No puedes pagar una compra no confirmada.")

    def enviar(self, compra):
        raise Exception("No puedes enviar una compra sin pagar.")

    def cancelar(self, compra):
        compra.estado = EstadoCancelada()
        print("Compra cancelada.")

class EstadoConfirmada(EstadoCompra):
    def __init__(self):
        self.nombre = EstadoCompraEnum.CONFIRMADA
    def confirmar(self, compra):
        raise Exception("La compra ya está confirmada.")
    
    def pagar(self, compra):
        compra.estado = EstadoPagada()
        print("Compra pagada.")
    
    def enviar(self, compra):
        raise Exception("No puedes enviar una compra que no ha sido pagada.")
    def cancelar(self, compra):
        raise Exception("No se puede cancelar una compra confirmada.")

class EstadoEnviada(EstadoCompra):
    def __init__(self):
        self.nombre = EstadoCompraEnum.ENVIADA
    def confirmar(self, compra):
        raise Exception("La compra ya está enviada.")
    
    def pagar(self, compra):
        raise Exception("La compra ya fue pagada.")
    
    def enviar(self, compra):
        raise Exception("La compra ya fue enviada.")
    def cancelar(self, compra):
        raise Exception("No se puede cancelar una compra enviada.")

class EstadoPagada(EstadoCompra):
    def __init__(self):
        self.nombre = EstadoCompraEnum.PAGADA
    def confirmar(self, compra):
        raise Exception("La compra ya está pagada.")
    
    def pagar(self, compra):
        raise Exception("La compra ya fue pagada.")
    
    def enviar(self, compra):
        compra.estado = EstadoEnviada()
        print("Compra enviada.")
    def cancelar(self, compra):
        raise Exception("No se puede cancelar una compra pagada.")
class EstadoCancelada(EstadoCompra):
    def __init__(self):
        self.nombre = EstadoCompraEnum.CANCELADA
    def confirmar(self, compra):
        raise Exception("La compra está cancelada y no se puede confirmar.")
    
    def pagar(self, compra):
        raise Exception("La compra está cancelada y no se puede pagar.")
    
    def enviar(self, compra):
        raise Exception("La compra está cancelada y no se puede enviar.")
    
    def cancelar(self, compra):
        raise Exception("La compra ya está cancelada.")