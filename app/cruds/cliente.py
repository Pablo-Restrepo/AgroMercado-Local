from uuid import UUID
from sqlalchemy import func
from sqlmodel import Session, select
from ..schemas.cliente import Cliente
from app.core.exceptions import ClienteNotFound


def create_cliente(
    session: Session,
    cliente: Cliente,
) -> Cliente:
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def get_clientes(
    session: Session,
    skip: int = 0,
    limit: int = 100,
) -> tuple[list[Cliente], int]:
    count_stmt = select(func.count()).select_from(Cliente)
    count = session.exec(count_stmt).one()

    stmt = select(Cliente).offset(skip).limit(limit)
    clientes = session.exec(stmt).all()

    return clientes, count


def get_cliente_by_id(
    session: Session,
    cliente_id: UUID,
) -> Cliente:
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise ClienteNotFound
    return cliente


def update_cliente(
    session: Session,
    cliente_id: UUID,
    cliente_in: Cliente,
) -> Cliente:
    cliente = get_cliente_by_id(session=session, cliente_id=cliente_id)

    update_data = cliente_in.model_dump(exclude_unset=True)
    cliente.sqlmodel_update(update_data)

    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def delete_cliente(
    session: Session,
    cliente_id: UUID,
) -> Cliente:
    cliente = get_cliente_by_id(session=session, cliente_id=cliente_id)
    session.delete(cliente)
    session.commit()
    return cliente

def get_cliente_by_cedula(session: Session, cedula: str) -> Cliente | None:
    stmt = select(Cliente).where(Cliente.cedula == cedula)
    return session.exec(stmt).first()
