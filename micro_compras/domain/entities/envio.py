from domain.entities.compra import Compra
from domain.entities.estado_envio import *
from datetime import datetime
from core.config import settings

class Envio:
    def __init__(self,id_gremio:int, compra: Compra,destino: str, valor : float=settings.DEFAULT_ENVIO_COST, id:int=None,estado:EstadoEnvio=EstadoPendiente(),fecha_envio: datetime = None):
        self.id = id
        #Campo para saber que gremio debe realizar el envio
        self.id_gremio = id_gremio
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
    def to_dict(self)-> dict:
        return {
            "id": self.id,
            "id_gremio": self.id_gremio,
            "compra": self.compra.to_dict() if self.compra else None,
            "destino": self.destino,
            "valor": self.valor,
            "estado": self.estado.nombre,
            "fecha_envio": self.fecha_envio.isoformat() if self.fecha_envio else None
        }
    