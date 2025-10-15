from fastapi import APIRouter, Depends, HTTPException
from application.services import GremioService
from application.dtos import CrearGremioDTO, GremioResponseDTO, ProductorResponseDTO
from deps import get_gremio_service 

router = APIRouter(prefix="/api/v1/gremios", tags=["Gremios"])

@router.post("/{id_admin}", response_model=GremioResponseDTO, status_code=201)
async def crear_gremio(id_admin: int, gremio: CrearGremioDTO, svc : GremioService = Depends(get_gremio_service)):
    try:
        return await svc.crear_gremio(id_admin, **gremio.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/{id}", response_model=GremioResponseDTO, status_code=200)
async def obtener_gremio(id: int, svc : GremioService = Depends(get_gremio_service)):
    try:
        return await svc.obtener_gremio(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/{id_gremio}/agregar/{id_productor}", response_model=ProductorResponseDTO, status_code=200)
async def agregar_productor_a_gremio(id_productor: int, id_gremio: int, svc : GremioService = Depends(get_gremio_service)):
    try:
        return await svc.agregar_productor_a_gremio(id_productor, id_gremio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id_gremio}/remover/{id_productor}", response_model=ProductorResponseDTO, status_code=200)
async def remover_productor_de_gremio(id_productor: int, id_gremio: int, svc : GremioService = Depends(get_gremio_service)):
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