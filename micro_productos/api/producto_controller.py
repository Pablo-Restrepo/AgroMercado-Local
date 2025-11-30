

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from core.auth_middleware import get_current_user
from .esquemas import CategoriaConsulta, ProductoRegistro, ProductoConsulta, ProductoActualizacion, RolEnum
from application.producto_service import ProductoService


class ProductoController:
    def __init__(self, service: ProductoService):
        self.router = APIRouter(prefix="/api/productos", tags=["Productos"])
        self.service = service

        # ---Mapear rutas a métodos---
        # rutas de comandos
        self.router.post("/", response_model=int)(self.registrar_producto)
        self.router.put("/{p_id}", response_model=int)(self.editar_producto)
        self.router.delete("/{p_id}", response_model=int)(self.eliminar_producto)
        # rutas de consultas
        self.router.get("/", response_model=List[ProductoConsulta])(self.listar_todos_los_productos)
        self.router.get("/gremio/{prod_cod_gremio}", response_model=List[ProductoConsulta])(self.listar_productos_por_gremio)
        self.router.get("/{p_id}", response_model=ProductoConsulta)(self.obtener_producto_por_id)
        self.router.get("/productor/{prod_id}", response_model=List[ProductoConsulta])(self.listar_por_productor)
        self.router.get("/categorias/",response_model=List[CategoriaConsulta])(self.listar_categorias)
        self.router.get("/categoria/{cat_id}",response_model=List[ProductoConsulta])(self.listar_todos_productos_por_categoria)
        self.router.get("/productor-categoria/{prod_id}/{cat_id}",response_model=List[ProductoConsulta])(self.listar_productos_por_categoria_productor)
        self.router.get("/gremio-categoria/{gre_id}/{cat_id}",response_model=List[ProductoConsulta])(self.listar_productos_por_categoria_gremio)
        self.router.get("/medicinales/",response_model=List[ProductoConsulta])(self.listar_todos_productos_medicinales)
        self.router.get("/gremio-medicinales/{gre_id}",response_model=List[ProductoConsulta])(self.listar_productos_medicinales_gremio)
        self.router.get("/productor-medicinales/{prod_id}",response_model=List[ProductoConsulta])(self.listar_productos_medicinales_productor)
    # ==========================================================
    # MÉTODOS DE COMANDO
    # ==========================================================
    async def registrar_producto(self, producto: ProductoRegistro,current_user: dict = Depends(get_current_user)) -> int:
        """
        Registra un nuevo producto (recibe un JSON).
        """
        if current_user.get('rol') == RolEnum.PRODUCTOR_ADMIN or current_user.get('rol') == RolEnum.PRODUCTOR_AFILIADO:
            producto_id = await self.service.registrar_producto(producto)
            return producto_id
        
        raise HTTPException(
                status_code=403,
                detail="No tiene permisos para registrar productos. Debe ser productor"
            )

    async def editar_producto(self, p_id: int, producto: ProductoActualizacion,current_user: dict = Depends(get_current_user)) -> int:
        """
        Edita un producto existente (recibe un JSON).
        """
        if current_user.get('rol') == RolEnum.PRODUCTOR_ADMIN or current_user.get('rol') == RolEnum.PRODUCTOR_AFILIADO:
            
            producto_id = await self.service.editar_producto(p_id, producto)
            return producto_id
        raise HTTPException(
                status_code=403,
                detail="No tiene permisos para editar productos. Debe ser productor"
            )

    async def eliminar_producto(self, p_id: int,current_user: dict = Depends(get_current_user)) -> int:
        """
        Elimina un producto por ID.
        """
        if current_user.get('rol') == RolEnum.PRODUCTOR_ADMIN or current_user.get('rol') == RolEnum.PRODUCTOR_AFILIADO:
            
            producto_id = await self.service.eliminar_producto(p_id)
            return producto_id
        raise HTTPException(
                status_code=403,
                detail="No tiene permisos para eliminar productos. Debe ser productor"
            )

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
    
    async def listar_categorias(self) ->List[CategoriaConsulta]: 
        return await self.service.listar_categorias()

    def listar_todos_productos_por_categoria(self,cat_id:int) -> List[ProductoConsulta]:
        return self.service.listar_todos_productos_por_categoria(cat_id)
    
    def listar_productos_por_categoria_gremio(self,gre_id:int,cat_id:int) -> List[ProductoConsulta]:
        return self.service.listar_productos_por_categoria_gremio(gre_id,cat_id)
   
    def listar_productos_por_categoria_productor(self,prod_id:int,cat_id:int) -> List[ProductoConsulta]:
        return self.service.listar_productos_por_categoria_productor(prod_id,cat_id)
    
    def listar_todos_productos_medicinales(self)  -> List[ProductoConsulta]:
        return self.service.listar_todos_productos_medicinales()
    
    def listar_productos_medicinales_gremio(self, gre_id:int)  -> List[ProductoConsulta]:
        return self.service.listar_productos_medicinales_gremio(gre_id)
    
    def listar_productos_medicinales_productor(self, prod_id:int)  -> List[ProductoConsulta]:
        return self.service.listar_productos_medicinales_productor(prod_id)
    
    
