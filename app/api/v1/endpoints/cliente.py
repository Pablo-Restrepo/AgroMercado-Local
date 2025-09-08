from uuid import UUID
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteRead, ClienteCreate, ClienteUpdate, ClienteList
from ....application.cliente_service import ClienteService
router = APIRouter(prefix='/clientes', tags=['clientes'])


@router.post('/', response_model=ClienteRead, status_code=201)
def create_cliente(
    session: SessionDep,
    cliente_in: ClienteCreate
) -> ClienteRead:
    cliente = Cliente.model_validate(cliente_in)
    return ClienteService.crear_cliente(session=session, cliente=cliente)


@router.get('/', response_model=ClienteList)
def get_clientes(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> ClienteList:
    clientes, count = ClienteService.obtener_clientes(
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
    return ClienteService.obtener_cliente_por_id(session=session, cliente_id=cliente_id)


@router.put('/{cliente_id}', response_model=ClienteRead)
def update_cliente(
    session: SessionDep,
    cliente_id: UUID,
    cliente_in: ClienteUpdate
) -> ClienteRead:
    return ClienteService.actualizar_cliente(
        session=session,
        cliente_id=cliente_id,
        cliente_in=cliente_in
    )


@router.delete('/{cliente_id}', response_model=ClienteRead)
def delete_cliente(
    session: SessionDep,
    cliente_id: UUID
) -> ClienteRead:
    return ClienteService.eliminar_cliente(session=session, cliente_id=cliente_id)

@router.get('/cedula/{cedula}', response_model=ClienteRead)
def get_cliente_by_cedula(
    session: SessionDep,
    cedula: str
) -> ClienteRead:
    cliente = ClienteService.obtener_cliente_por_cedula(session, cedula)
    if not cliente:
        # Puedes lanzar una excepción personalizada si lo deseas
        from app.core.exceptions import ClienteNotFound
        raise ClienteNotFound
    return cliente
