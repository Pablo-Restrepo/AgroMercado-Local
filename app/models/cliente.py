from .base import SQLModel
from sqlmodel import Relationship


class Cliente(SQLModel, table=True):
    cedula: str
    nombre: str
    apellido: str
    direccion: str

    pedidos: list['Pedido'] = Relationship(back_populates='cliente')
