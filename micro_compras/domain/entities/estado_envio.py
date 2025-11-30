from abc import ABC, abstractmethod
from enum import Enum
class EstadoEnvioEnum(str, Enum):
    PENDIENTE = "PENDIENTE"
    DESPACHADO = "DESPACHADO"
    EN_RUTA = "EN_RUTA"
    ENTREGADO = "ENTREGADO"
class EstadoEnvio(ABC):
    @abstractmethod
    def despachar(self, envio): ...
    @abstractmethod
    def en_ruta(self, envio): ...
    @abstractmethod
    def entregado(self, envio): ...

class EstadoPendiente(EstadoEnvio):
    def __init__(self):
        self.nombre = EstadoEnvioEnum.PENDIENTE
    def despachar(self, envio):
        envio.estado = EstadoDespachado()
        print("El envío fue despachado.")
    def en_ruta(self, envio): raise Exception("El envío aún no ha sido despachado.")
    def entregado(self, envio): raise Exception("El envío aún no ha sido despachado.")

class EstadoDespachado(EstadoEnvio):
    def __init__(self):
        self.nombre = EstadoEnvioEnum.DESPACHADO
    def despachar(self, envio): raise Exception("El envío ya fue despachado.")
    def en_ruta(self, envio):
        envio.estado = EstadoEnRuta()
        print("El envío está en ruta.")
    def entregado(self, envio): raise Exception("El envío aún no está en ruta.")

class EstadoEnRuta(EstadoEnvio):
    def __init__(self):
        self.nombre = EstadoEnvioEnum.EN_RUTA
    def despachar(self, envio): raise Exception("Ya está en ruta.")
    def en_ruta(self, envio): raise Exception("Ya está en ruta.")
    def entregado(self, envio):
        envio.estado = EstadoEntregado()
        print("El envío fue entregado.")

class EstadoEntregado(EstadoEnvio):
    def __init__(self):
        self.nombre = EstadoEnvioEnum.ENTREGADO
    def despachar(self, envio): raise Exception("El envío ya fue entregado.")
    def en_ruta(self, envio): raise Exception("El envío ya fue entregado.")
    def entregado(self, envio): raise Exception("El envío ya fue entregado.")
