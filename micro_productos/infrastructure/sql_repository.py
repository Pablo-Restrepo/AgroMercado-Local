
from api.esquemas import ProductoRegistro, ProductoActualizacion, ProductorRegistroConsulta
from infrastructure.int_command_repository import IProductoCommandRepository
from infrastructure.db.sql_engine import async_session
from infrastructure.sql_models import ProductoModel, ProductorModel
from infrastructure.logging import logger
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
import base64
class SQLCommandRepository(IProductoCommandRepository):


    async def save_producto(self, producto:ProductoRegistro)-> int:
        async with async_session() as session:
            imagen = base64.b64decode(producto.img)
            producto_model = ProductoModel(p_nombre=producto.p_nombre,p_precio = producto.p_precio, prod_id = producto.prod_id,
                                           p_tipo=producto.p_tipo, p_unidad=producto.p_unidad, p_stock=producto.p_stock, imagen=imagen)
            session.add(producto_model)
            await session.commit()
            await session.refresh(producto_model)            
            logger.info(f"Producto agregado: {producto.p_nombre} (id={producto_model.p_id})")
            return producto_model.p_id

    async def save_productor(self, productor: ProductorRegistroConsulta) -> int:
        async with async_session() as session:
            productor_model = ProductorModel(prod_nombre=productor.prod_nombre,prod_apellido = productor.prod_apellido, prod_id = productor.prod_id,
                                            prod_cod_gremio = productor.prod_cod_gremio, prod_nombre_gremio = productor.prod_nombre_gremio)
            session.add(productor_model)
            await session.commit()
            await session.refresh(productor_model)            
            logger.info(f"Productor agregado: {productor.prod_nombre} {productor.prod_apellido} (id={productor_model.prod_id})")
            return productor_model.prod_id
    async def edit_producto(self,p_id: int, producto: ProductoActualizacion) -> int:
        async with async_session() as session:
            # Buscar el producto existente
            db_producto = await session.get(ProductoModel, p_id)
            if not db_producto:
                logger.warning(f"Producto con id={p_id} no encontrado")
                return 0  # o puedes lanzar una excepción

            # Actualizar los campos
            db_producto.p_nombre = producto.p_nombre
            db_producto.p_precio = producto.p_precio
            db_producto.p_tipo = producto.p_tipo
            db_producto.p_unidad = producto.p_unidad
            db_producto.imagen = producto.img
            db_producto.p_stock = producto.p_stock


            # Confirmar los cambios
            await session.commit()
            await session.refresh(db_producto)

            logger.info(f"Producto actualizado: {db_producto.p_nombre} (id={db_producto.p_id})")
            return db_producto.p_id

    async def get_productor(self, prod_id: int) -> ProductorRegistroConsulta:
        """Obtiene un productor por su ID desde la base de datos SQL"""
        async with async_session() as session:
            productor_model = await session.get(ProductorModel,prod_id)

            if not productor_model:
                return None

            # Convertir el modelo SQL al modelo de dominio
            return ProductorRegistroConsulta(
                prod_id=productor_model.prod_id,
                prod_nombre=productor_model.prod_nombre,
                prod_apellido=productor_model.prod_apellido,
                prod_nombre_gremio=productor_model.prod_nombre_gremio,
                prod_cod_gremio=productor_model.prod_cod_gremio
            )
    async def delete_producto(self,p_id: int) -> int:
        """
        Elimina un producto por su ID.
        Retorna:
            1 si se eliminó correctamente,
            0 si no se encontró,
        -1 si ocurrió un error.
        """
        async with async_session() as session:
            try:

                db_producto = await session.get(ProductoModel, p_id)
                if not db_producto:
                    logger.warning(f"Producto con id={p_id} no encontrado")
                    return 0  # o puedes lanzar una excepción
                # Confirmar la transacción
                db_producto.p_estado = False
                await session.commit()
                logger.info(f"Producto con id={p_id} eliminado correctamente.")
                return 1

            except SQLAlchemyError as e:
                logger.error(f"Error al eliminar el producto con id={p_id}: {e}")
                await session.rollback()
                return -1


