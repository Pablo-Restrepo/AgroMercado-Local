from domain.models import Gremio, Productor
from domain.repository import IGremioRepository, IProductorRepository
from application.dtos import GremioResponseDTO, ProductorResponseDTO

class ProductorService:
    def __init__(self, productor_repo: IProductorRepository):        
        self.productor_repo = productor_repo
    # Métodos del servicio
    async def crear_productor(self, id, codigo, nombres, apellidos, id_gremio=None, rol=None) -> ProductorResponseDTO:
        # Validaciones de negocio
        if not id or not codigo or not nombres or not apellidos:
            raise ValueError("Todos los campos son obligatorios")
        # TO DO: Validar que el código sea único (requiere acceso al repositorio)
        productor = Productor(id=id, codigo=codigo, nombres=nombres, apellidos=apellidos, id_gremio=id_gremio, rol=rol)
        try:
            await self.productor_repo.agregar_productor(productor)
        except Exception as e:
            raise ValueError("Error insertando el productor")
        return ProductorResponseDTO.model_validate(productor,from_attributes=True)
    async def listar_productores(self) -> list[ProductorResponseDTO]:
        productores = await self.productor_repo.obtener_productores()
        return [ProductorResponseDTO.model_validate(p,from_attributes=True) for p in productores if p.es_activo]
    async def obtener_productor(self, id) -> ProductorResponseDTO:
        productor = await self.productor_repo.obtener_productor_por_id(id)
        if not productor:
            raise ValueError("Productor no encontrado")
        return ProductorResponseDTO.model_validate(productor,from_attributes=True)
    async def eliminar_productor(self, id):
        productor = await self.productor_repo.obtener_productor_por_id(id)
        if not productor:
            raise ValueError("Productor no encontrado")
        productor.eliminar_productor()
        await self.productor_repo.actualizar_productor(productor)
        return ProductorResponseDTO.model_validate(productor,from_attributes=True)
class GremioService:
    def __init__(self, gremio_repo: IGremioRepository, productor_repo: IProductorRepository):
        self.gremio_repo = gremio_repo
        self.productor_repo = productor_repo
    # Métodos del servicio
    async def crear_gremio(self, id_admin:int, id:int, nombre:str) -> GremioResponseDTO:
        # Validaciones de negocio
        if not id or not nombre or not id_admin:
            raise ValueError("Todos los campos son obligatorios")
        # TO DO: Validar que el nombre sea único (requiere acceso al repositorio)
        try:
            admin = await self.productor_repo.obtener_productor_por_id(id_admin)
            gremio = admin.crear_gremio(id, nombre)
            await self.gremio_repo.agregar_gremio(gremio)
            await self.productor_repo.actualizar_productor(admin)
        except Exception as e:
            raise ValueError(f"Error creando el gremio: {e}")                                
        return GremioResponseDTO.model_validate(gremio,from_attributes=True)
    
    async def agregar_productor_a_gremio(self, id_productor, id_gremio):        
        productor = await self.productor_repo.obtener_productor_por_id(id_productor)
        if not productor:
            raise ValueError("Productor no encontrado")
        gremio = await self.gremio_repo.obtener_gremio_por_id(id_gremio)
        if not gremio:
            raise ValueError("Gremio no encontrado")
        gremio.agregar_productor(productor)
        await self.productor_repo.actualizar_productor(productor)
        return ProductorResponseDTO.model_validate(productor,from_attributes=True)
    async def remover_productor_de_gremio(self, id_productor, id_gremio):
        productor = await self.productor_repo.obtener_productor_por_id(id_productor)
        if not productor:
            raise ValueError("Productor no encontrado")
        gremio = await self.gremio_repo.obtener_gremio_por_id(id_gremio)
        if not gremio:
            raise ValueError("Gremio no encontrado")
        try:
            gremio.remover_productor(productor)
        except ValueError as e:
            raise ValueError(f"No se puede remover el productor del gremio: {e}")
        await self.productor_repo.actualizar_productor(productor)
        return ProductorResponseDTO.model_validate(productor,from_attributes=True)
    async def listar_gremios(self) -> list[GremioResponseDTO]:
        gremios = await self.gremio_repo.obtener_gremios()
        if not gremios:
            raise ValueError("No hay gremios registrados")
        return [GremioResponseDTO.model_validate(g,from_attributes=True) for g in gremios]
    async def obtener_gremio(self, id) -> GremioResponseDTO:
        gremio = await self.gremio_repo.obtener_gremio_por_id(id)
        if not gremio:
            raise ValueError("Gremio no encontrado")
        return GremioResponseDTO.model_validate(gremio,from_attributes=True)
    async def listar_productores_por_gremio(self, id_gremio) -> list[ProductorResponseDTO]:
        gremio = await self.gremio_repo.obtener_gremio_por_id(id_gremio)
        if not gremio:
            raise ValueError("Gremio no encontrado")
        return [ProductorResponseDTO.model_validate(p,from_attributes=True) for p in await self.gremio_repo.obtener_productores_por_gremio(id_gremio)]