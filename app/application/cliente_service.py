from sqlmodel import Session
from uuid import UUID
from ..schemas.cliente import Cliente
from ..cruds.cliente import (
    create_cliente,
    get_clientes,
    get_cliente_by_id,
    update_cliente,
    delete_cliente, get_cliente_by_cedula
)

class ClienteService:
    @staticmethod
    def crear_cliente(session: Session, cliente: Cliente) -> Cliente:
        return create_cliente(session, cliente)

    @staticmethod
    def obtener_clientes(session: Session, skip: int = 0, limit: int = 100) -> tuple[list[Cliente], int]:
        return get_clientes(session, skip, limit)

    @staticmethod
    def obtener_cliente_por_id(session: Session, cliente_id: UUID) -> Cliente:
        return get_cliente_by_id(session, cliente_id)

    @staticmethod
    def actualizar_cliente(session: Session, cliente_id: UUID, cliente_in: Cliente) -> Cliente:
        return update_cliente(session, cliente_id, cliente_in)

    @staticmethod
    def eliminar_cliente(session: Session, cliente_id: UUID) -> Cliente:
        return delete_cliente(session, cliente_id)
    
    @staticmethod
    def obtener_cliente_por_cedula(session: Session, cedula: str) -> Cliente | None:
        return get_cliente_by_cedula(session, cedula)