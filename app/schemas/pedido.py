from datetime import datetime
from sqlmodel import SQLModel, Field,Relationship
from uuid import UUID, uuid4
from typing import Optional, List
from ..models.pedido import Pedido as PedidoModel
from pydantic import field_validator
from .producto_unitario import ProductoUnitarioRead
class PedidoBase(SQLModel):
    cliente_cedula: str = Field(description="cedula del cliente que realiza el pedido")
    fecha_pedido: datetime = Field(description="Fecha en que se realizó el pedido")
    estado: str = Field(
        min_length=2,
        max_length=20,
        description="Estado del pedido"
    )
    total: float = Field(description="Total del pedido")
    

class PedidoCreate(SQLModel):
    productos: dict[str, int] = Field(
        description="Diccionario de productos y sus cantidades")

class PedidoRead(PedidoBase):
    id: UUID
    productos_unitarios: List[ProductoUnitarioRead] = []

class PedidoList(SQLModel):
    data: list[PedidoRead]
    count: int

class PedidoUpdate(PedidoBase):
    cliente_cedula: str | None
    fecha_pedido: datetime | None
    estado: str | None
    total: float | None

class Pedido(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    cliente_cedula: str = Field(description="cedula del cliente que realiza el pedido")
    fecha_pedido: datetime = Field(description="Fecha en que se realizó el pedido")
    estado: str = Field(
        min_length=2,
        max_length=20,
        description="Estado del pedido"
    )
    total: float = Field(description="Total del pedido")
    productos_unitarios: List["ProductoUnitario"] = Relationship(
    back_populates="pedido",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    @classmethod
    def from_model(cls, pedido_model:PedidoModel):
        return cls(
            cliente_cedula=pedido_model.cliente.cedula,
            fecha_pedido=pedido_model.fecha_pedido,
            estado=pedido_model.estado.name,
            total=pedido_model.valor_total
        )