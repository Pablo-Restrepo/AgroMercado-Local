

from fastapi import APIRouter, HTTPException, status
from typing import List
from .esquemas import ProductoRegistro, ProductoConsulta, ProductoActualizacion
from application.producto_service import ProductoService


class ProductoController:
    def __init__(self, service: ProductoService):
        self.router = APIRouter(prefix="/productos", tags=["Productos"])
        self.service = service

        # Mapear rutas a métodos
        self.router.post("/", response_model=int)(self.registrar_producto)
        self.router.put("/{p_id}", response_model=int)(self.editar_producto)
        self.router.delete("/{p_id}", response_model=int)(self.eliminar_producto)
        self.router.get("/", response_model=List[ProductoConsulta])(self.listar_todos_los_productos)
        self.router.get("/gremio/{prod_cod_gremio}", response_model=List[ProductoConsulta])(self.listar_productos_por_gremio)
        self.router.get("/{p_id}", response_model=ProductoConsulta)(self.obtener_producto_por_id)
        self.router.get("/productor/{prod_id}", response_model=List[ProductoConsulta])(self.listar_por_productor)

    # ==========================================================
    # MÉTODOS DE COMANDO
    # ==========================================================
    async def registrar_producto(self, producto: ProductoRegistro) -> int:
        """
        Registra un nuevo producto (recibe un JSON).
        """
        producto_id = await self.service.registrar_producto(producto)
        return producto_id

    async def editar_producto(self, p_id: int, producto: ProductoActualizacion) -> int:
        """
        Edita un producto existente (recibe un JSON).
        """
        producto_id = await self.service.editar_producto(p_id, producto)
        return producto_id

    async def eliminar_producto(self, p_id: int) -> int:
        """
        Elimina un producto por ID.
        """
        producto_id = await self.service.eliminar_producto(p_id)
        return producto_id

    # ==========================================================
    # MÉTODOS DE CONSULTA
    # ==========================================================
    def listar_todos_los_productos(self) -> List[ProductoConsulta]:
        """
        Retorna todos los productos.
        """
        return self.service.listar_todos_los_productos()

    def listar_productos_por_gremio(self, prod_cod_gremio: int) -> List[ProductoConsulta]:
        """
        Retorna los productos asociados a un gremio.
        """
        return self.service.listar_productos_por_gremio(prod_cod_gremio)

    def obtener_producto_por_id(self, p_id: int) -> ProductoConsulta:
        """
        Retorna un producto específico por ID.
        """
        producto = self.service.obtener_producto_por_id(p_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return producto
    
    def listar_por_productor(self, prod_id: int):
        return self.service.listar_productos_por_productor(prod_id)
    
    
