#Implementación de los repositorios

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from domain.models import Productor, Gremio
from domain.repository import IProductorRepository, IGremioRepository
from infra.db.models_orm import ProductorORM, GremioORM
from infra.db.base import async_session
from infra.logging import logger

class GremioRepositorySQL(IGremioRepository):
    async def agregar_gremio(self, gremio: Gremio):
        async with async_session() as session:
            nuevo_gremio = GremioORM(id=gremio.id, nombre=gremio.nombre)
            session.add(nuevo_gremio)
            await session.commit()
            logger.info(f"Gremio agregado: {gremio.nombre}")

    async def obtener_gremios(self) -> list[Gremio]:
        async with async_session() as session:
            #Se debe usar selectinload para cargar los productores, sino se hace se generan problemas por temas asincronos
            #Esto se llama eager loading
            result = await session.execute(
                select(GremioORM).options(selectinload(GremioORM.productores))
            )
            gremios_orm = result.scalars().all()
            return [
                Gremio(
                    id=row.id,
                    nombre=row.nombre,
                    productores=[
                        Productor(
                            id=p.id,
                            codigo=p.codigo,
                            nombres=p.nombres,
                            apellidos=p.apellidos,
                            id_gremio=row.id,
                            rol=p.rol,
                            es_activo=p.es_activo == "TRUE"
                        )
                        for p in row.productores
                    ]
                )
                for row in gremios_orm
            ]

    async def obtener_gremio_por_id(self, id) -> Gremio:
        async with async_session() as session:
            result = await session.execute(
                select(GremioORM).where(GremioORM.id == id).options(selectinload(GremioORM.productores))
            )
            orm = result.scalars().first()
            if orm:
                productores = [
                Productor(
                    id=p.id,                    
                    codigo=p.codigo,
                    nombres=p.nombres,
                    apellidos=p.apellidos,
                    id_gremio=orm.id,
                    rol=p.rol,
                    es_activo=p.es_activo == "TRUE"
                )
                for p in orm.productores
                ]
                return Gremio(id=orm.id, nombre=orm.nombre, productores=productores)
            logger.warning(f"Gremio no encontrado: {id}")
            return None

    async def obtener_productores_por_gremio(self, id_gremio) -> list[Productor]:
        async with async_session() as session:
            result = await session.execute(
                select(GremioORM).where(GremioORM.id == id_gremio).options(selectinload(GremioORM.productores))
            )
            orm = result.scalars().first()
            logger.info(f"Obteniendo productores para gremio: {orm}")
            if orm:
                return [
                    Productor(
                        id=p.id,                
                        codigo=p.codigo,
                        nombres=p.nombres,
                        apellidos=p.apellidos,
                        id_gremio=orm.id,
                        rol=p.rol,
                        es_activo=p.es_activo == "TRUE"
                    )
                    for p in orm.productores
                ]
            logger.warning(f"Gremio no encontrado para obtener productores: {id_gremio}")
            return []
class ProductorRepositorySQL(IProductorRepository):
    async def agregar_productor(self, productor: Productor):
        async with async_session() as session:
            try:    
                nuevo_productor = ProductorORM(
                    id=productor.id,
                    codigo=productor.codigo, 
                    nombres=productor.nombres,
                    apellidos=productor.apellidos,                   
                    rol=productor.rol if productor.rol else "None",
                    gremio_id=productor.id_gremio if productor.id_gremio else "None",
                    es_activo="TRUE" if productor.es_activo else "FALSE"
                )
                session.add(nuevo_productor)
                await session.commit()
                logger.info(f"Productor agregado: {productor.codigo}")
            except Exception as e:
                await session.rollback()
                logger.error(f"Error al agregar productor: {e}")
                raise

    async def obtener_productores(self) -> list[Productor]:
        async with async_session() as session:
            result = await session.execute(
                select(ProductorORM)
            )
            productores_orm = result.fetchall()
            productores = [row[0] for row in productores_orm]
            logger.info(f"Productores obtenidos: {len(productores_orm)}")
            return [
                Productor(
                    id=row.id,
                    codigo=row.codigo,
                    nombres=row.nombres,  
                    apellidos=row.apellidos,
                    id_gremio=row.gremio_id if row.gremio_id != "None" else None,
                    rol=row.rol if row.rol != "None" else None,
                    es_activo=row.es_activo == "TRUE"
                )
                for row in productores
            ]

    async def obtener_productor_por_id(self, id) -> Productor:
        async with async_session() as session:
            orm = await session.get(ProductorORM, id)
            if orm:
                return Productor(
                    id=orm.id,
                    codigo=orm.codigo,
                    nombres=orm.nombres,
                    apellidos=orm.apellidos,
                    id_gremio=orm.gremio_id if orm.gremio_id != "None" else None,
                    rol=orm.rol if orm.rol != "None" else None,
                    es_activo=orm.es_activo == "TRUE"
                )
            logger.warning(f"Productor no encontrado: {id}")
            return None

    async def actualizar_productor(self, productor: Productor):
        async with async_session() as session:
            orm = await session.get(ProductorORM, productor.id)
            if orm:
                orm.codigo = productor.codigo
                orm.nombres = productor.nombres
                orm.apellidos = productor.apellidos
                orm.es_activo = "TRUE" if productor.es_activo else "FALSE"
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
                orm.es_activo = "FALSE"
                orm.gremio_id = "None"
                orm.rol = "None"
                await session.commit()
                logger.info(f"Productor eliminado: {id}")
            else:
                logger.warning(f"Productor no encontrado para eliminar: {id}")
