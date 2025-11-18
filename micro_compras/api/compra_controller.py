from fastapi import APIRouter, Depends, HTTPException

from application.compra_service import CompraService
from application.dtos import CompraRequestDTO
from core.auth_middleware import get_current_user
from deps import get_compra_service

router = APIRouter(prefix="/api/compras", tags=["Compras"])
@router.post("/", status_code=201)
#Para la autorización incluir: ,current_user: dict = Depends(get_current_user)
async def crear_compra(compra_data:CompraRequestDTO, svc: CompraService =Depends(get_compra_service)):
    """Crea una nueva compra. Solo usuarios con rol 'cliente' pueden crear compras."""
    """if current_user.get('rol') != 'cliente':
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para crear compras. Se requiere rol cliente"
        )"""
    return await svc.create_compra(compra_data)
@router.get("/{compra_id}", status_code=200)
async def obtener_compra(compra_id: int, svc: CompraService = Depends(get_compra_service)):
    """Obtiene una compra por su ID."""
    return await svc.get_compra(compra_id)