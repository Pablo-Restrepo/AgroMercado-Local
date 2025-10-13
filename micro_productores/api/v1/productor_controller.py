from fastapi import APIRouter, Depends, HTTPException
from application.services import ProductorService
from application.dtos import CrearProductorDTO, ProductorResponseDTO
from deps import get_productor_service

router = APIRouter(prefix="/api/v1/productores", tags=["Productores"])

@router.post("/", response_model=ProductorResponseDTO, status_code=201)
async def crear_productor(productor: CrearProductorDTO, svc : ProductorService = Depends(get_productor_service)):
    try:
        return await svc.crear_productor(**productor.model_dump())
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
@router.delete("/{id}", response_model=ProductorResponseDTO, status_code=200)
async def eliminar_productor(id: int, svc : ProductorService = Depends(get_productor_service)):
    try:
        return await svc.eliminar_productor(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))