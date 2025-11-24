"""Implementación de los repositorios"""
#Implementación de los repositorios
from sqlmodel import select
from domain.entities.producto import Producto
from domain.entities.producto_unitario import ProductoUnitario
from domain.exceptions import DomainError
from domain.repository import *
from infraestructure.db.modelsSQL import *
from infraestructure.db.engine import async_session
from infraestructure.logging import logger
from sqlalchemy.orm import selectinload
from infraestructure.db.mapper import *

class UsuarioRepository(IUsuarioRepository):
    async def get_usuario_by_id(self, u_id: int) -> Optional[Usuario]:
        async with async_session() as session:
            result = await session.execute(select(UsuarioModel).where(UsuarioModel.u_id == u_id))
            usuario_model = result.scalar_one_or_none()
            if usuario_model:
                return Usuario(
                    id=usuario_model.u_id,
                    nombre=usuario_model.u_nombre,
                    email=usuario_model.u_email,
                    es_activo=usuario_model.u_es_activo
                )
            logger.warning(f"Usuario con id {u_id} no encontrado.")
            return None
    async def save_usuario(self, usuario: Usuario):
        async with async_session() as session:
            usuario_model = UsuarioModel(
                u_nombre=usuario.nombre,
                u_email=usuario.email,
                u_es_activo=usuario.es_activo
            )
            session.add(usuario_model)
            await session.commit()
            await session.refresh(usuario_model)
            usuario.id = usuario_model.u_id
            logger.info(f"Usuario guardado con id {usuario.id}.")
            return usuario
    async def get_usuario_by_email(self, email: str) -> Optional[Usuario]:
        async with async_session() as session:
            result = await session.execute(select(UsuarioModel).where(UsuarioModel.u_email == email))
            usuario_model = result.scalar_one_or_none()
            if usuario_model:
                return Usuario(
                    id=usuario_model.u_id,
                    nombre=usuario_model.u_nombre,
                    email=usuario_model.u_email,
                    es_activo=usuario_model.u_es_activo
                )            
            logger.warning(f"Usuario con email {email} no encontrado.")
            return None
class ProductoRepository(IProductoRepository):
    async def get_producto_by_id(self, p_id: int) -> Optional[Producto]:
        async with async_session() as session:
            result = await session.execute(select(ProductoModel).where(ProductoModel.p_id == p_id))
            producto_model = result.scalar_one_or_none()
            if producto_model:
                return Producto(
                    id=producto_model.p_id,
                    nombre=producto_model.p_nombre,
                    id_gremio=producto_model.p_id_gremio,
                    precio=producto_model.p_precio,
                    unidad=producto_model.p_unidad,
                    stock=producto_model.p_stock
                )
            logger.warning(f"Producto con id {p_id} no encontrado.")
            return None
    async def save_producto(self, producto):
        async with async_session() as session:
            producto_model = ProductoModel(
                p_nombre=producto.nombre,
                p_id_gremio=producto.id_gremio,
                p_precio=producto.precio,
                p_unidad=producto.unidad,
                p_stock=producto.stock
            )
            session.add(producto_model)
            await session.commit()
            await session.refresh(producto_model)
            producto.id = producto_model.p_id
            logger.info(f"Producto guardado con id {producto.id}.")
            return producto
    async def get_productos(self)-> List[Producto]:
        async with async_session() as session:
            result = await session.execute(select(ProductoModel))
            productos_models = result.scalars().all()
            productos = [
                Producto(
                    id=prod.p_id,
                    nombre=prod.p_nombre,
                    id_gremio=prod.p_id_gremio,
                    precio=prod.p_precio,
                    unidad=prod.p_unidad,
                    stock=prod.p_stock
                ) for prod in productos_models
            ]
            logger.info(f"{len(productos)} productos obtenidos.")
            return productos
class ProductoUnitarioRepository(IProductoUnitarioRepository):
    async def save_producto_unitario(self, producto_unitario: ProductoUnitario):
        async with async_session() as session:
            producto_unitario_model = producto_unitario_entity_to_model(producto_unitario)
            session.add(producto_unitario_model)
            await session.commit()
            await session.refresh(producto_unitario_model)
            producto_unitario.id = producto_unitario_model.pu_id
            logger.info(f"Producto unitario guardado con id {producto_unitario.id}.")
            return producto_unitario    
    async def get_productos_unitarios_by_compra(self, id_compra:int) -> List[ProductoUnitario]:
        async with async_session() as session:
            result = await session.execute(
                select(ProductoUnitarioModel).where(ProductoUnitarioModel.c_id == id_compra)
            )
            productos_unitarios_models = result.scalars().all()
            productos_unitarios = [
                producto_unitario_model_to_entity(pu) for pu in productos_unitarios_models                
            ]
            logger.info(f"{len(productos_unitarios)} productos unitarios obtenidos para la compra {id_compra}.")
            return productos_unitarios
class CompraRepository(ICompraRepository):
    async def save_compra(self, compra:Compra)-> Compra:
        """
        Guarda la compra + items y reduce stock de cada producto en la misma transacción.
        Lanza DomainError en caso de producto no encontrado o stock insuficiente.
        """
        async with async_session() as session:
            async with session.begin():  # asegura transacción
                # 1) Validar y bloquear filas de producto (pessimistic lock)
                for pu in compra.productos:
                    result = await session.execute(
                        select(ProductoModel).where(ProductoModel.p_id == pu.id_producto).with_for_update()
                    )
                    prod_model = result.scalar_one_or_none()
                    if not prod_model:
                        raise DomainError(f"Producto con ID {pu.id_producto} no existe", code="PRODUCT_NOT_FOUND", status_code=404)
                    if prod_model.p_stock < pu.cantidad:
                        raise DomainError(f"Stock insuficiente para el producto ID {pu.id_producto}", code="INSUFFICIENT_STOCK", status_code=400)
                    # reducir stock en memoria (se persistirá al hacer commit)
                    prod_model.p_stock = prod_model.p_stock - pu.cantidad
                    session.add(prod_model)

                # 2) Crear compra SIN productos (evitar duplicados)
                compra_model = CompraModel(
                    u_id=compra.id_usuario,
                    c_fecha=compra.fecha,
                    c_total=compra.total,
                    c_estado=compra.estado.nombre
                )
                session.add(compra_model)
                await session.flush()  # asegura que compra_model.c_id exista

                # 3) Crear y persistir producto_unitario asociados a la compra
                for pu in compra.productos:
                    pu_model = producto_unitario_entity_to_model(pu)
                    pu_model.c_id = compra_model.c_id
                    session.add(pu_model)

                # al salir del context manager se hace commit; si ocurre excepción, se hace rollback

            # refrescar
            await session.refresh(compra_model)
            logger.info(f"Compra guardada con id {compra_model.c_id}.")
            compra = await self.get_compra_by_id(compra_model.c_id)
            return compra
    async def get_compras(self) -> List[Compra]:
        async with async_session() as session:
            result = await session.execute(
                select(CompraModel).options(
                    selectinload(CompraModel.c_productos),
                    selectinload(CompraModel.c_envio)
                )
            )
            compras_models = result.scalars().all()
            compras = [compra_model_to_entity(c) for c in compras_models]
            logger.info(f"{len(compras)} compras obtenidas.")
            return compras
    async def get_compra_by_id(self, id:int)-> Compra:
        async with async_session() as session:
            result = await session.execute(
                select(CompraModel).where(CompraModel.c_id == id).options(
                    selectinload(CompraModel.c_productos),
                    selectinload(CompraModel.c_envio)
                )
            )
            compra_model = result.scalar_one_or_none()
            logger.info(f"Buscando compra con id {id}.")
            if compra_model:
                compra = compra_model_to_entity(compra_model)
                logger.info(f"Compra con id {id} obtenida.")
                return compra
            logger.warning(f"Compra con id {id} no encontrada.")
            return None
    async def get_compras_by_usuario(self, id_usuario:int) -> List[Compra]:
        async with async_session() as session:
            result = await session.execute(
                select(CompraModel).where(CompraModel.u_id == id_usuario).options(
                    selectinload(CompraModel.c_productos),
                    selectinload(CompraModel.c_envio)
                )
            )
            compras_models = result.scalars().all()
            compras = [compra_model_to_entity(c) for c in compras_models]
            logger.info(f"{len(compras)} compras obtenidas para el usuario {id_usuario}.")
            return compras
    async def update_compra(self, compra:Compra):
        async with async_session() as session:
            compra_model = await session.get(CompraModel, compra.id)
            if not compra_model:
                logger.warning(f"Compra con id {compra.id} no encontrada para actualizar.")
                return None
            # Actualizar campos
            compra_model.c_estado = compra.estado.nombre
            await session.commit()
            logger.info(f"Compra con id {compra.id} actualizada.")
            return compra
class EnvioRepository(IEnvioRepository):
    async def save_envio(self, envio:Envio):
        async with async_session() as session:            
            envio_model = envio_entity_to_model(envio)
            session.add(envio_model)
            await session.commit()
            await session.refresh(envio_model)
            envio.id = envio_model.e_id
            logger.info(f"Envío guardado con id {envio.id}.")
            return envio
    async def get_envio_by_id(self, id:int) -> Optional[Envio]:
        async with async_session() as session:
            result = await session.execute(
                select(EnvioModel).where(EnvioModel.e_id == id).options(
                    selectinload(EnvioModel.e_compra).selectinload(CompraModel.c_productos)
                )
            )
            envio_model = result.scalar_one_or_none()
            if envio_model:                
                envio = envio_model_to_entity(envio_model)
                logger.info(f"Envío con id {id} obtenido.")
                return envio
            logger.warning(f"Envío con id {id} no encontrado.")
            return None
    async def update_envio(self, envio:Envio):
        async with async_session() as session:
            envio_model = await session.get(EnvioModel, envio.id)
            if not envio_model:
                logger.warning(f"Envío con id {envio.id} no encontrado para actualizar.")
                return None
            # Actualizar campos            
            envio_model.e_estado = envio.estado.nombre
            envio_model.e_fecha_envio = envio.fecha_envio
            await session.commit()
            logger.info(f"Envío con id {envio.id} actualizado.")
            return envio
    async def get_envios_by_id_gremio(self, id_gremio:int) -> List[Envio]:
        async with async_session() as session:
            result = await session.execute(
                select(EnvioModel).where(EnvioModel.e_id_gremio == id_gremio).options(
                    selectinload(EnvioModel.e_compra).selectinload(CompraModel.c_productos)
                )
            )
            envios_models = result.scalars().all()            
            envios = [envio_model_to_entity(e) for e in envios_models]
            logger.info(f"{len(envios)} envíos obtenidos para el gremio {id_gremio}.")
            return envios
    async def get_envios_by_usuario(self, id_usuario:int) -> List[Envio]:
        async with async_session() as session:
            result = await session.execute(
                select(EnvioModel).join(CompraModel).where(CompraModel.u_id == id_usuario).options(
                    selectinload(EnvioModel.e_compra).selectinload(CompraModel.c_productos)
                )
            )
            envios_models = result.scalars().all()            
            envios = [envio_model_to_entity(e) for e in envios_models]
            logger.info(f"{len(envios)} envíos obtenidos para el usuario {id_usuario}.")
            return envios
