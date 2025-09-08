from uuid import UUID
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoRead, PedidoCreate, PedidoUpdate, PedidoList
from app.application.pedido_service import PedidoService


router = APIRouter(prefix='/pedidos', tags=['pedidos'])

@router.post('/{cedula_cli}', response_model=PedidoRead, status_code=201)
def create_pedido(
    session: SessionDep,
    pedido_in: PedidoCreate, cedula_cli: str
) -> PedidoRead:
    return PedidoService.crear_pedido(session, pedido_in, cedula_cli)

@router.get('/', response_model=PedidoList)
def get_pedidos(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> PedidoList:
    pedidos = PedidoService.obtener_pedidos(session, skip, limit)
    return PedidoList(data=pedidos, count=len(pedidos))

@router.get('/{pedido_id}', response_model=PedidoRead)
def get_pedido_by_id(
    session: SessionDep,
    pedido_id: UUID,
) -> PedidoRead:
    return PedidoService.obtener_pedido(session, pedido_id)

@router.put('/{pedido_id}', response_model=PedidoRead)
def update_pedido(
    session: SessionDep,
    pedido_id: UUID,
    pedido_in: PedidoUpdate
) -> PedidoRead:
    return PedidoService.actualizar_pedido(session, pedido_id, pedido_in.dict(exclude_unset=True))

@router.delete('/{pedido_id}', response_model=PedidoRead)
def delete_pedido(
    session: SessionDep,
    pedido_id: UUID
) -> PedidoRead:
    return PedidoService.eliminar_pedido(session, pedido_id)

@router.get('/cliente/{cedula}', response_model=PedidoList)
def get_pedidos_por_cedula(
    session: SessionDep,
    cedula: str
) -> PedidoList:
    pedidos = PedidoService.obtener_pedidos_por_cedula(session, cedula)
    return PedidoList(data=pedidos, count=len(pedidos))