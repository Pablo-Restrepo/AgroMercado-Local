from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.producto import Producto
from app.schemas.producto import ProductoRead, ProductoCreate, ProductoUpdate
from app.application.producto_service import ProductoService

router = APIRouter(prefix='/productos', tags=['productos'])

@router.get('/', response_model=list[ProductoRead])
def get_productos(session: SessionDep, skip: int = 0, limit: int = 100):
    return ProductoService.obtener_productos(session, skip, limit)

@router.get('/{producto_id}', response_model=ProductoRead)
def get_producto(session: SessionDep, producto_id: int):
    return ProductoService.obtener_producto(session, producto_id)

@router.post('/', response_model=ProductoRead, status_code=201)
def create_producto(session: SessionDep, producto_in: ProductoCreate):
    producto = Producto.model_validate(producto_in)
    return ProductoService.crear_producto(session, producto)

@router.put('/{producto_id}', response_model=ProductoRead)
def update_producto(session: SessionDep, producto_id: int, producto_in: ProductoUpdate):
    return ProductoService.actualizar_producto(session, producto_id, producto_in.dict(exclude_unset=True))

@router.delete('/{producto_id}', response_model=ProductoRead)
def delete_producto(session: SessionDep, producto_id: int):
    return ProductoService.eliminar_producto(session, producto_id)

@router.get('/buscar/{nombre}', response_model=list[ProductoRead])
def buscar_productos_por_nombre(session: SessionDep, nombre: str):
    return ProductoService.obtener_productos_por_nombre(session, nombre)