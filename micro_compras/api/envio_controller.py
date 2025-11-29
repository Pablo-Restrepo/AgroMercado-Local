from fastapi import APIRouter, Depends, HTTPException

from application.services import EnvioService
from core.auth_middleware import get_current_user
from deps import get_envio_service
from domain.entities.estado_envio import EstadoEnvioEnum
from domain.entities.usuario import RolEnum


router = APIRouter(prefix="/api/envios", tags=["Envios"])
@router.get("/gremio/{gremio_id}", status_code=200)
async def get_envios_by_gremio(gremio_id: int, svc: EnvioService = Depends(get_envio_service),current_user: dict = Depends(get_current_user)):
    """Obtiene todos los envíos de un gremio."""
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para ver estos envíos. Se requiere rol admin de gremio"
        )
    return await svc.get_envios_por_gremio(gremio_id)
@router.get("/usuario/{usuario_id}", status_code=200)
async def get_envios_by_usuario(usuario_id: int, svc: EnvioService = Depends(get_envio_service), current_user: dict = Depends(get_current_user)):
    """Obtiene todos los envíos del usuario autenticado."""
    if int(current_user.get('user_id')) != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para ver estos envíos."
        )
    return await svc.get_envios_por_usuario(usuario_id)
@router.patch("/{envio_id}", status_code=200)
async def update_envio(
    envio_id: int, 
    status: EstadoEnvioEnum,
    svc: EnvioService = Depends(get_envio_service), current_user: dict = Depends(get_current_user)):
    """Actualiza el estado de un envío por su ID."""
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para actualizar envíos. Se requiere rol admin de gremio"
        )
    return await svc.update_envio_status(envio_id, status)