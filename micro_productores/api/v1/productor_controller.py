from fastapi import APIRouter, Depends, HTTPException
from application.services import ProductorService
from application.dtos import ProductorResponseDTO, RegistrarProductorEnGremioDTO
from deps import get_productor_service
from core.auth_middleware import get_current_user
from domain.models import RolEnum

router = APIRouter(prefix="/api/productores", tags=["Productores"])

@router.post("/", response_model=ProductorResponseDTO, status_code=201)
async def crear_productor(productor: RegistrarProductorEnGremioDTO, current_user: dict = Depends(get_current_user), svc : ProductorService = Depends(get_productor_service)):

    # Verificar que el usuario tiene rol productor-admin
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para registrar productores en gremios. Se requiere rol productor-admin"
        )

    try:
        return await svc.crear_productor(productor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/", response_model=list[ProductorResponseDTO], status_code=200)
async def listar_productores(svc : ProductorService = Depends(get_productor_service)):
    try:
        return await svc.listar_productores()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/{id}", response_model=ProductorResponseDTO, status_code=200)
async def obtener_productor(id: int, svc : ProductorService = Depends(get_productor_service)):
    try:
        return await svc.obtener_productor(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/user/{user_id}", response_model=ProductorResponseDTO, status_code=200)
async def obtener_productor_por_user_id(user_id: int, svc : ProductorService = Depends(get_productor_service)):
    try:
        return await svc.obtener_productor_por_user_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}", response_model=ProductorResponseDTO, status_code=200)
async def eliminar_productor(id: int, svc : ProductorService = Depends(get_productor_service)):
    try:
        return await svc.eliminar_productor(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))