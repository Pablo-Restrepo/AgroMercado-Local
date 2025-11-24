from fastapi import APIRouter, Depends, HTTPException

from application.services import CompraService
from application.dtos import CompraRequestDTO
from core.auth_middleware import get_current_user
from deps import get_compra_service,get_envio_service
from domain.entities.usuario import RolEnum

router = APIRouter(prefix="/api/compras", tags=["Compras"])
@router.post("/", status_code=201)
#Para la autorización incluir: ,current_user: dict = Depends(get_current_user)
async def create_compra(compra_data:CompraRequestDTO, svc: CompraService =Depends(get_compra_service),current_user: dict = Depends(get_current_user)):
    """Crea una nueva compra. Solo usuarios con rol 'cliente' pueden crear compras."""
    if current_user.get('rol') != RolEnum.CLIENTE:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para crear compras. Se requiere rol cliente"
        )
    return await svc.create_compra(compra_data)
@router.get("/{compra_id}", status_code=200)
async def get_compra(compra_id: int, svc: CompraService = Depends(get_compra_service)):
    """Obtiene una compra por su ID."""
    return await svc.get_compra(compra_id)
@router.get("/usuario/{usuario_id}", status_code=200)
async def get_compras_by_usuario(usuario_id: int, svc: CompraService = Depends(get_compra_service), current_user: dict = Depends(get_current_user)):
    """Obtiene todas las compras del usuario autenticado."""
    if current_user.get('id') != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para ver estas compras."
        )
    return await svc.get_compras_by_usuario(usuario_id)
@router.post("/{compra_id}/confirmar", status_code=200)
async def confirmar_compra(compra_id: int, svc: CompraService = Depends(get_compra_service), current_user: dict = Depends(get_current_user)):
    if current_user.get('rol') != RolEnum.CLIENTE:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para confirmar compras. Se requiere rol cliente"
        )
    """Confirma una compra por su ID."""
    return await svc.confirmar_compra(compra_id)
@router.post("/{compra_id}/pagar", status_code=200)
async def pagar_compra(compra_id: int, destino: str, svc: CompraService = Depends(get_compra_service), current_user: dict = Depends(get_current_user)):
    """Marca una compra como pagada por su ID."""
    if current_user.get('rol') != RolEnum.CLIENTE:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para pagar compras. Se requiere rol cliente"
        )
    return await svc.pagar_compra(compra_id, destino,get_envio_service())
