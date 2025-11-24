
import base64

from bson import Binary
from api.esquemas import ProductoActualizacion, ProductoCompra, ProductoRegistro, ProductoConsulta, ProductorRegistroConsulta
from core.events import event_manager
from infrastructure.int_command_repository import IProductoCommandRepository
from infrastructure.int_query_repository import IProductoQueryRepository
from core.events import publisher, queue_creacion_productos, queue_actualizacion_productos


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
        
        #construir los datos para db de mongo
        event_data = {
            "p_id": producto_id,
            "p_nombre": producto_datos.p_nombre,
            "p_tipo": producto_datos.p_tipo,
            "p_unidad": producto_datos.p_unidad,
            "p_precio": producto_datos.p_precio,
            "p_stock": producto_datos.p_stock,
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

        # publicar producto registrado en la cola

        # construir los datos de producto para publicar en la cola
        producto_cola = {
            "id": producto_id,
            "nombre": producto_datos.p_nombre,
            "unidad": producto_datos.p_unidad,
            "precio": producto_datos.p_precio,
            "stock": producto_datos.p_stock
        }
        await publisher.publish(message=producto_cola,routing_key=queue_creacion_productos)
        return producto_id
    async def registrar_productor(self, productor_data:ProductorRegistroConsulta):
        return await self.command_repo.save_productor(productor_data)

    async def editar_producto(self, p_id: int, producto_datos: ProductoActualizacion) -> int:
        """
        Actualiza los datos de un producto existente.
        Retorna el id del producto editado.
        """
        producto_original = self.query_repo.get_producto_por_id(p_id=p_id)
        producto_id =  await self.command_repo.edit_producto(p_id, producto=producto_datos)
        producto_modificado = self.query_repo.get_producto_por_id(p_id=producto_id)

        if producto_original != producto_modificado:
            #construir la informacion para el evento de actualizacion en mongo db
            event_data = {
                "p_id": producto_id,
                "p_nombre": producto_datos.p_nombre,
                "p_tipo": producto_datos.p_tipo,
                "p_unidad": producto_datos.p_unidad,
                "p_precio": producto_datos.p_precio,
                "p_stock": producto_datos.p_stock,
                "imagen":producto_datos.img
            }
            # Notificar evento
            await event_manager.notify("producto_actualizado", event_data)
            # publicar el producto en la cola
            # solo se publica el evento a la cola si cambia alguno de estos campos
            # nombre, unidad,precio o stock 
            campos_a_verificar = ["p_nombre", "p_unidad", "p_precio", "p_stock"]

            cambio = any(
                getattr(producto_original, campo) != getattr(producto_modificado, campo)
                for campo in campos_a_verificar
            )

            if cambio:
                producto_cola = {
                    "id": producto_id,
                    "nombre": producto_datos.p_nombre,
                    "unidad": producto_datos.p_unidad,
                    "precio": producto_datos.p_precio,
                    "stock": producto_datos.p_stock
                }
                await publisher.publish(message=producto_cola,routing_key=queue_actualizacion_productos)
        return producto_id

    async def actualizar_stock_productos(self, productos_compra:list[ProductoCompra]) -> int:

        producto_actualizados = []
        lista_dicts_compras = []
        for producto in productos_compra:
            id_producto_actualizado = await self.command_repo.edit_producto_stock(producto.p_id, producto.cant)
            producto_actualizados.append(id_producto_actualizado)
            lista_dicts_compras.append(producto.model_dump())
        
        # Notificar evento
        await event_manager.notify("producto_stock_actualizado", lista_dicts_compras)
        return len(producto_actualizados)




    async def eliminar_producto(self, p_id: int) -> int:
        """
        Elimina un producto de la base de datos.
        Retorna el id del producto eliminado.
        """
        await event_manager.notify("producto_eliminado", p_id)
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
