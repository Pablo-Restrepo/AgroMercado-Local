from uuid import UUID
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteRead, ClienteCreate, ClienteUpdate, ClienteList
from app.cruds import cliente as crud

router = APIRouter(prefix='/clientes', tags=['clientes'])


@router.post('/', response_model=ClienteRead, status_code=201)
def create_cliente(
    session: SessionDep,
    cliente_in: ClienteCreate
) -> ClienteRead:
    cliente = Cliente.model_validate(cliente_in)
    return crud.create_cliente(session=session, cliente=cliente)


@router.get('/', response_model=ClienteList)
def get_clientes(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> ClienteList:
    clientes, count = crud.get_clientes(
        session=session,
        skip=skip,
        limit=limit
    )
    return ClienteList(data=clientes, count=count)


@router.get('/{cliente_id}', response_model=ClienteRead)
def get_cliente_by_id(
    session: SessionDep,
    cliente_id: UUID,
) -> ClienteRead:
    return crud.get_cliente_by_id(session=session, cliente_id=cliente_id)


@router.put('/{cliente_id}', response_model=ClienteRead)
def update_cliente(
    session: SessionDep,
    cliente_id: UUID,
    cliente_in: ClienteUpdate
) -> ClienteRead:
    return crud.update_cliente(
        session=session,
        cliente_id=cliente_id,
        cliente_in=cliente_in
    )


@router.delete('/{cliente_id}', response_model=ClienteRead)
def delete_cliente(
    session: SessionDep,
    cliente_id: UUID
) -> ClienteRead:
    return crud.delete_cliente(session=session, cliente_id=cliente_id)
