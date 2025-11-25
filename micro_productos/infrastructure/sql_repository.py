
from api.esquemas import CategoriaConsulta, CategoriaRegistro, ProductoCompra, ProductoRegistro, ProductoActualizacion, ProductorRegistroConsulta
from infrastructure.int_command_repository import IProductoCommandRepository
from infrastructure.db.sql_engine import async_session
from infrastructure.mongo_collections import Categoria
from infrastructure.sql_models import CategoriaModel, ProductoModel, ProductorModel
from infrastructure.logging import logger
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
import base64
class SQLCommandRepository(IProductoCommandRepository):


    async def save_producto(self, producto:ProductoRegistro)-> int:
        async with async_session() as session:
            imagen = base64.b64decode(producto.img)
            producto_model = ProductoModel(p_nombre=producto.p_nombre,p_precio = producto.p_precio, prod_id = producto.prod_id,p_medicinal= producto.p_medicinal,
                                           cat_id=producto.cat_id, p_unidad=producto.p_unidad, p_stock=producto.p_stock, imagen=imagen)
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
            db_producto.cat_id = producto.cat_id
            db_producto.p_unidad = producto.p_unidad
            db_producto.p_medicinal = producto.p_medicinal
            imagen = base64.b64decode(producto.img)
            db_producto.imagen = imagen
            db_producto.p_stock = producto.p_stock


            # Confirmar los cambios
            await session.commit()
            await session.refresh(db_producto)

            logger.info(f"Producto actualizado: {db_producto.p_nombre} (id={db_producto.p_id})")
            return db_producto.p_id
        
    async def edit_producto_stock(self, p_id: int, cant:int) -> int:
        async with async_session() as session:
            # Buscar el producto existente
            db_producto = await session.get(ProductoModel, p_id)
            if not db_producto:
                logger.warning(f"Producto con id={p_id} no encontrado")
                return 0  # o puedes lanzar una excepción
            stock_actual = db_producto.p_stock
            if stock_actual < cant:
                logger.error(f"Error, la cantidad comprada del producto {p_id} ({cant}), supera al stock actual: {stock_actual}")
                raise ValueError("la cantidad comprada no puede ser superior al stock actual")
            nuevo_stock = stock_actual - cant
            db_producto.p_stock = nuevo_stock

            # Confirmar los cambios
            await session.commit()
            await session.refresh(db_producto)

            logger.info(f"el stock del producto actualizado: {db_producto.p_nombre} (id={db_producto.p_id})")
            return db_producto.p_id
    
    async def save_categoria(self, categoria: CategoriaRegistro) -> int:
        async with async_session() as session:
            categoria_model = CategoriaModel(cat_nombre=categoria.cat_nombre)
            session.add(categoria_model)
            await session.commit()
            await session.refresh(categoria_model)            
            logger.info(f"Ctegoria agregado: {categoria.cat_nombre} (id={categoria_model.cat_id})")
            return categoria_model.cat_id

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
        
    async def get_categoria(self, cat_id:int) -> CategoriaConsulta:
        async with async_session() as session:
            categoria_model = await session.get(CategoriaModel,cat_id)
            
            if not categoria_model:
                return None
            
            return CategoriaConsulta(cat_id= categoria_model.cat_id,cat_nombre=categoria_model.cat_nombre)
    
    async def get_categorias(self) -> list[CategoriaConsulta]:
        async with async_session() as session:
            stmt = select(CategoriaModel)
            result = await session.execute(stmt)

            categorias_model = result.scalars().all()

            categorias = [
                CategoriaConsulta(cat_id=c.cat_id, cat_nombre=c.cat_nombre)
                for c in categorias_model
            ]
            return categorias
            

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


