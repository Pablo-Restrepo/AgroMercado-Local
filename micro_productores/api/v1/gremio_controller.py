from fastapi import APIRouter, Depends, HTTPException
from application.services import GremioService
from application.dtos import CrearGremioDTO, GremioResponseDTO, ProductorResponseDTO
from deps import get_gremio_service 
from core.auth_middleware import get_current_user
from domain.models import RolEnum

router = APIRouter(prefix="/api/gremios", tags=["Gremios"])

@router.post("/{id_admin}", response_model=GremioResponseDTO, status_code=201)
async def crear_gremio(id_admin: int, gremio: CrearGremioDTO, current_user: dict = Depends(get_current_user), svc: GremioService = Depends(get_gremio_service)):
    # Verificar que el usuario tiene rol productor-admin
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para crear gremios. Se requiere rol productor-admin"
        )

    try:
        return await svc.crear_gremio(id_admin, gremio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/{id}", response_model=GremioResponseDTO, status_code=200)
async def obtener_gremio(id: int, svc : GremioService = Depends(get_gremio_service)):
    try:
        return await svc.obtener_gremio(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/{id_gremio}/agregar/{id_productor}", response_model=ProductorResponseDTO, status_code=200)
async def agregar_productor_a_gremio(id_productor: int, id_gremio: int, current_user: dict = Depends(get_current_user), svc : GremioService = Depends(get_gremio_service)):
    # Verificar que el usuario tiene rol productor-admin
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para agregar productores a gremios. Se requiere rol productor-admin"
        )
    try:
        return await svc.agregar_productor_a_gremio(id_productor, id_gremio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id_gremio}/remover/{id_productor}", response_model=ProductorResponseDTO, status_code=200)
async def remover_productor_de_gremio(id_productor: int, id_gremio: int, current_user: dict = Depends(get_current_user), svc : GremioService = Depends(get_gremio_service)):
    # Verificar que el usuario tiene rol productor-admin
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para remover productores de gremios. Se requiere rol productor-admin"
        )
    try:
        return await svc.remover_productor_de_gremio(id_productor, id_gremio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/", response_model=list[GremioResponseDTO], status_code=200)
async def listar_gremios(svc : GremioService = Depends(get_gremio_service)):
    try:
        return await svc.listar_gremios()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))