


from sqlmodel import select
from api.esquemas import ProductoRegistro, ProductoActualizacion
from domain import Productor
from domain.Producto import Producto
from infrastructure.int_command_repository import IProductoCommandRepository
from infrastructure.db.sql_engine import async_session
from sqlalchemy.orm import selectinload
from infrastructure.sql_models import ProductoModel, ProductorModel
from infrastructure.logging import logger
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

class SQLCommandRepository(IProductoCommandRepository):


    async def save_producto(producto:ProductoRegistro)-> int:
        async with async_session() as session:
            producto_model = ProductoModel(p_nombre=producto.p_nombre,p_precio = producto.p_precio,
                                           p_tipo=producto.p_tipo, p_unidad=producto.p_unidad)
            session.add(producto_model)
            await session.commit()
            await session.refresh(producto_model)            
            logger.info(f"Producto agregado: {producto.p_nombre} (id={producto_model.p_id})")
            return producto_model.p_id

    async def edit_producto(p_id: int, producto: ProductoActualizacion) -> int:
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

            # Confirmar los cambios
            await session.commit()
            await session.refresh(db_producto)

            logger.info(f"Producto actualizado: {db_producto.p_nombre} (id={db_producto.p_id})")
            return db_producto.p_id

    async def get_productor(self, prod_id: int) -> Productor:
        """Obtiene un productor por su ID desde la base de datos SQL"""
        result = await self._session.execute(
            select(ProductorModel).where(ProductorModel.id == prod_id)
        )
        productor_model = result.scalar_one_or_none()

        if not productor_model:
            return None

        # Convertir el modelo SQL al modelo de dominio
        return Productor(
            id=productor_model.id,
            nombre=productor_model.nombre,
            apellido=productor_model.apellido,
            correo=productor_model.correo,
            telefono=productor_model.telefono
        )
    async def delete_producto(p_id: int) -> int:
        """
        Elimina un producto por su ID.
        Retorna:
            1 si se eliminó correctamente,
            0 si no se encontró,
        -1 si ocurrió un error.
        """
        async with async_session() as session:
            try:
                # Ejecutar la sentencia DELETE
                stmt = delete(ProductoModel).where(ProductoModel.p_id == p_id)
                result = await session.execute(stmt)

                # Confirmar la transacción
                await session.commit()

                # result.rowcount indica cuántas filas fueron afectadas
                if result.rowcount == 0:
                    logger.warning(f"Producto con id={p_id} no encontrado.")
                    return 0

                logger.info(f"Producto con id={p_id} eliminado correctamente.")
                return 1

            except SQLAlchemyError as e:
                logger.error(f"Error al eliminar el producto con id={p_id}: {e}")
                await session.rollback()
                return -1


