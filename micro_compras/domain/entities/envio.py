from domain.entities.compra import Compra
from domain.entities.estado_envio import *
from datetime import datetime

class Envio:
    def __init__(self, id:int, compra: Compra,destino: str, valor : int, estado:EstadoEnvio=EstadoPendiente(),fecha_envio: datetime = None):
        self.id = id
        self.compra = compra
        self.destino = destino  
        self.valor = valor
        self.estado = estado
        self.fecha_envio = fecha_envio
    #Esta lógica debería ser manipulada por el admin del gremio pertinente    
        
    def despachar_envio(self):
        self.estado.despachar(self)
        self.fecha_envio = datetime.now()
    def enviar_en_ruta(self):
        self.estado.en_ruta(self)
    def entregar_envio(self):
        self.estado.entregado(self)
    
    