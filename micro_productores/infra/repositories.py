#Implementación de los repositorios
from sqlmodel import select
from domain.models import Productor, Gremio
from domain.repository import IProductorRepository, IGremioRepository
from infra.db.modelsSQL import ProductorModel, GremioModel
from infra.db.engine import async_session
from infra.logging import logger
from sqlalchemy.orm import selectinload


# Repositorio para gremios usando SQLModel (async)
class GremioRepositorySQL(IGremioRepository):
    async def agregar_gremio(self, gremio: Gremio) -> int:
        async with async_session() as session:
            gremio_model = GremioModel(gre_nombre=gremio.nombre)
            session.add(gremio_model)
            await session.commit()
            await session.refresh(gremio_model)            
            logger.info(f"Gremio agregado: {gremio.nombre} (id={gremio_model.gre_id})")
            return gremio_model.gre_id

    async def obtener_gremios(self) -> list[Gremio]:
        async with async_session() as session:
            result = await session.execute(
                select(GremioModel).options(selectinload(GremioModel.productores))
            )
            gremios_orm = result.scalars().all()
            return [
                Gremio(
                    id=g.gre_id,
                    nombre=g.gre_nombre,
                    productores=[
                        Productor(
                            id=p.prod_id,
                            codigo=p.prod_codigo,
                            nombres=p.prod_nombres,
                            apellidos=p.prod_apellidos,
                            id_gremio=g.gre_id,
                            rol=(p.prod_rol if p.prod_rol != "NONE" else None),
                            es_activo=bool(p.prod_es_activo)
                        )
                        for p in g.productores
                    ]
                )
                for g in gremios_orm
            ]

    async def obtener_gremio_por_id(self, id) -> Gremio:
        async with async_session() as session:
            result = await session.execute(
                select(GremioModel).where(GremioModel.gre_id == id).options(selectinload(GremioModel.productores))
            )
            gremio = result.scalars().first()
            if gremio:
                productores = [
                    Productor(
                        id=p.prod_id,
                        codigo=p.prod_codigo,
                        nombres=p.prod_nombres,
                        apellidos=p.prod_apellidos,
                        id_gremio=gremio.gre_id,
                        rol=(p.prod_rol if p.prod_rol != "NONE" else None),
                        es_activo=bool(p.prod_es_activo)
                    )
                    for p in gremio.productores
                ]
                return Gremio(id=gremio.gre_id, nombre=gremio.gre_nombre, productores=productores)
            logger.warning(f"Gremio no encontrado: {id}")
            return None

    async def obtener_productores_por_gremio(self, id_gremio) -> list[Productor]:
        async with async_session() as session:
            result = await session.execute(
                select(GremioModel).where(GremioModel.gre_id == id_gremio).options(selectinload(GremioModel.productores))
            )
            orm = result.scalars().first()
            logger.info(f"Obteniendo productores para gremio: {orm}")
            if orm:
                return [
                    Productor(
                        id=p.prod_id,
                        codigo=p.prod_codigo,
                        nombres=p.prod_nombres,
                        apellidos=p.prod_apellidos,
                        id_gremio=orm.gre_id,
                        rol=(p.prod_rol if p.prod_rol != "NONE" else None),
                        es_activo=bool(p.prod_es_activo)
                    )
                    for p in orm.productores
                ]
            logger.warning(f"Gremio no encontrado para obtener productores: {id_gremio}")
            return []


class ProductorRepositorySQL(IProductorRepository):
    async def agregar_productor(self, productor: Productor):
        async with async_session() as session:
            try:
                nuevo = ProductorModel(
                    prod_codigo=productor.codigo,
                    prod_nombres=productor.nombres,
                    prod_apellidos=productor.apellidos,
                    prod_rol=(productor.rol if productor.rol else "NONE"),
                    gre_id=productor.id_gremio if productor.id_gremio is not None else None,
                    prod_es_activo=bool(productor.es_activo)
                )
                session.add(nuevo)
                await session.commit()
                await session.refresh(nuevo)
                logger.info(f"Productor agregado: {productor.codigo} (id={nuevo.prod_id})")
                return nuevo.prod_id
            except Exception as e:
                await session.rollback()
                logger.error(f"Error al agregar productor: {e}")
                raise

    async def obtener_productores(self) -> list[Productor]:
        async with async_session() as session:
            result = await session.execute(select(ProductorModel))
            productores_orm = result.scalars().all()
            logger.info(f"Productores obtenidos: {len(productores_orm)}")
            return [
                Productor(
                    id=p.prod_id,
                    codigo=p.prod_codigo,
                    nombres=p.prod_nombres,
                    apellidos=p.prod_apellidos,
                    id_gremio=(p.gre_id if p.gre_id is not None else None),
                    rol=(p.prod_rol if p.prod_rol != "NONE" else None),
                    es_activo=bool(p.prod_es_activo)
                )
                for p in productores_orm
            ]

    async def obtener_productor_por_id(self, id) -> Productor:
        async with async_session() as session:
            orm = await session.get(ProductorModel, id)
            if orm:
                return Productor(
                    id=orm.prod_id,
                    codigo=orm.prod_codigo,
                    nombres=orm.prod_nombres,
                    apellidos=orm.prod_apellidos,
                    id_gremio=(orm.gre_id if orm.gre_id is not None else None),
                    rol=(orm.prod_rol if orm.prod_rol != "NONE" else None),
                    es_activo=bool(orm.prod_es_activo)
                )
            logger.warning(f"Productor no encontrado: {id}")
            return None

    async def actualizar_productor(self, productor: Productor):
        async with async_session() as session:
            orm = await session.get(ProductorModel, productor.id)
            if orm:
                orm.prod_codigo = productor.codigo
                orm.prod_nombres = productor.nombres
                orm.prod_apellidos = productor.apellidos
                orm.prod_es_activo = bool(productor.es_activo)
                orm.prod_rol = (productor.rol if productor.rol else "NONE")
                orm.gre_id = (productor.id_gremio if productor.id_gremio is not None else None)
                await session.commit()
                logger.info(f"Productor actualizado: {productor.id}")
            else:
                logger.warning(f"Productor no encontrado para actualizar: {productor.id}")

    async def eliminar_productor(self, id):
        async with async_session() as session:
            orm = await session.get(ProductorModel, id)
            if orm:
                # marcar como inactivo en lugar de borrar
                orm.prod_es_activo = False
                orm.gre_id = None
                orm.prod_rol = "NONE"
                await session.commit()
                logger.info(f"Productor eliminado (soft): {id}")
            else:
                logger.warning(f"Productor no encontrado para eliminar: {id}")
    
    async def es_codigo_existente(self, codigo: str) -> bool:        
        # Si no hay código explícito, permitir (no existe conflicto)
        if not codigo:
            return False
        async with async_session() as session:
            result = await session.execute(select(ProductorModel).where(ProductorModel.prod_codigo == codigo))
            return result.first() is not None