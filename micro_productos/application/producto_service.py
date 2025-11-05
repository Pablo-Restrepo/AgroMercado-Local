
import base64

from bson import Binary
from api.esquemas import ProductoRegistro, ProductoConsulta, ProductorRegistroConsulta
from core.events import event_manager
from infrastructure.int_command_repository import IProductoCommandRepository
from infrastructure.int_query_repository import IProductoQueryRepository

class ProductoService:
    def __init__(self, command_repo: IProductoCommandRepository, query_repo: IProductoQueryRepository):
        """
        Servicio de aplicación que orquesta operaciones sobre productos
        utilizando CQRS (comandos y consultas separados).
        """
        self.command_repo = command_repo
        self.query_repo = query_repo

    # ==========================================================
    # MÉTODOS DE COMANDO (escritura)
    # ==========================================================
    async def registrar_producto(self, producto_datos: ProductoRegistro) -> int:
        """
        Registra un nuevo producto en la base de datos.
        Retorna el id del producto creado.
        """
        producto_id = await self.command_repo.save_producto(producto=producto_datos)
        productor:ProductorRegistroConsulta = await self.command_repo.get_productor(prod_id=producto_datos.prod_id)
        
        event_data = {
            "p_id": producto_id,
            "p_nombre": producto_datos.p_nombre,
            "p_tipo": producto_datos.p_tipo,
            "p_unidad": producto_datos.p_unidad,
            "p_precio": producto_datos.p_precio,
            "imagen":producto_datos.img,
            "productor": {
                "prod_id": producto_datos.prod_id,
                "prod_nombre": productor.prod_nombre,
                "prod_apellido": productor.prod_apellido,
                "prod_cod_gremio":productor.prod_cod_gremio,
                "prod_nombre_gremio": productor.prod_nombre_gremio
            }
        }

        # Notificar evento
        await event_manager.notify("producto_creado", event_data)

        return producto_id
    async def registrar_productor(self, productor_data:ProductorRegistroConsulta):
        return await self.command_repo.save_productor(productor_data)

    async def editar_producto(self, p_id: int, producto_datos: ProductoRegistro) -> int:
        """
        Actualiza los datos de un producto existente.
        Retorna el id del producto editado.
        """
        return await self.command_repo.edit_producto(p_id, Producto=producto_datos)

    async def eliminar_producto(self, p_id: int) -> int:
        """
        Elimina un producto de la base de datos.
        Retorna el id del producto eliminado.
        """
        return await self.command_repo.delete_producto(p_id=p_id)

    # ==========================================================
    # MÉTODOS DE CONSULTA (lectura)
    # ==========================================================
    def listar_todos_los_productos(self) -> list[ProductoConsulta]:
        """
        Retorna una lista con todos los productos.
        """
        return self.query_repo.list_all_productos()

    def listar_productos_por_gremio(self, prod_cod_gremio: int) -> list[ProductoConsulta]:
        """
        Retorna los productos asociados a un gremio específico.
        """
        return self.query_repo.list_productos_por_gremio(prod_cod_gremio)

    def obtener_producto_por_id(self, p_id: int) -> ProductoConsulta:
        """
        Retorna un producto específico por su ID.
        """
        return self.query_repo.get_producto_por_id(p_id=p_id)

    def listar_productos_por_productor(self, prod_id: int) -> list[ProductoConsulta]:
        return  self.query_repo.list_productos_por_productor(prod_id=prod_id)
