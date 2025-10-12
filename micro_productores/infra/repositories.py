#Implementación de los repositorios

from sqlalchemy import select
from domain.models import Productor, Gremio
from domain.repository import IProductorRepository, IGremioRepository
from infra.db.models_orm import ProductorORM, GremioORM
from infra.db.base import async_session
from logging import logger
class GremioRepositorySQL(IGremioRepository):
    async def agregar_gremio(self, gremio: Gremio):
        async with async_session() as session:
            nuevo_gremio = GremioORM(id=gremio.id, nombre=gremio.nombre)
            session.add(nuevo_gremio)
            await session.commit()
            logger.info(f"Gremio agregado: {gremio.nombre}")

    async def obtener_gremios(self) -> list[Gremio]:
        async with async_session() as session:
            result = await session.execute(
                select(GremioORM)
            )
            gremios_orm = result.fetchall()
            logger.info(f"Gremios obtenidos: {len(gremios_orm)}")
            return [Gremio(id=row.id, nombre=row.nombre) for row in gremios_orm]

    async def obtener_gremio_por_id(self, id) -> Gremio:
        async with async_session() as session:
            orm = await session.get(GremioORM, id)
            if orm:
                productores = [
                Productor(
                    id=p.id,
                    persona_id=p.persona_id,
                    codigo=p.codigo,
                    rol=p.rol,
                    gremio_id=orm.id,
                )
                for p in orm.productores
                ]
                return Gremio(id=orm.id, nombre=orm.nombre, productores=productores)
            logger.warning(f"Gremio no encontrado: {id}")
            return None

    async def obtener_productores_por_gremio(self, id_gremio) -> list[Productor]:
        async with async_session() as session:
            orm = await session.get(GremioORM, id_gremio)
            if orm:
                return [
                    Productor(
                        id=p.id,
                        persona_id=p.persona_id,
                        codigo=p.codigo,
                        rol=p.rol,
                        gremio_id=orm.id,
                    )
                    for p in orm.productores
                ]
            logger.warning(f"Gremio no encontrado para obtener productores: {id_gremio}")
            return []
class ProductorRepositorySQL(IProductorRepository):
    async def agregar_productor(self, productor: Productor):
        async with async_session() as session:
            nuevo_productor = ProductorORM(
                id=productor.id,
                codigo=productor.codigo,
                persona_id=productor.id,
                rol=productor.rol if productor.rol else "None",
                gremio_id=productor.id_gremio if productor.id_gremio else "None",
            )
            session.add(nuevo_productor)
            await session.commit()
            logger.info(f"Productor agregado: {productor.codigo}")

    async def obtener_productores(self) -> list[Productor]:
        async with async_session() as session:
            result = await session.execute(
                select(ProductorORM)
            )
            productores_orm = result.fetchall()
            logger.info(f"Productores obtenidos: {len(productores_orm)}")
            return [
                Productor(
                    id=row.id,
                    codigo=row.codigo,
                    nombres="",  # TO DO: Fetch from Persona service
                    apellidos="",  # TO DO: Fetch from Persona service
                    id_gremio=row.gremio_id if row.gremio_id != "None" else None,
                    rol=row.rol if row.rol != "None" else None,
                )
                for row in productores_orm
            ]

    async def obtener_productor_por_id(self, id) -> Productor:
        async with async_session() as session:
            orm = await session.get(ProductorORM, id)
            if orm:
                return Productor(
                    id=orm.id,
                    codigo=orm.codigo,
                    nombres="",  # TO DO: Fetch from Persona service
                    apellidos="",  # TO DO: Fetch from Persona service
                    id_gremio=orm.gremio_id if orm.gremio_id != "None" else None,
                    rol=orm.rol if orm.rol != "None" else None,
                )
            logger.warning(f"Productor no encontrado: {id}")
            return None

    async def actualizar_productor(self, productor: Productor):
        async with async_session() as session:
            orm = await session.get(ProductorORM, productor.id)
            if orm:
                orm.codigo = productor.codigo
                orm.rol = productor.rol if productor.rol else "None"
                orm.gremio_id = productor.id_gremio if productor.id_gremio else "None"
                await session.commit()
                logger.info(f"Productor actualizado: {productor.codigo}")
            else:
                logger.warning(f"Productor no encontrado para actualizar: {productor.id}")

    async def eliminar_productor(self, id):
        async with async_session() as session:
            orm = await session.get(ProductorORM, id)
            if orm:
                await session.delete(orm)
                await session.commit()
                logger.info(f"Productor eliminado: {id}")
            else:
                logger.warning(f"Productor no encontrado para eliminar: {id}")
