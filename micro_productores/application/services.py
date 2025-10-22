from domain.repository import IGremioRepository, IProductorRepository
from application.dtos import CrearProductorDTO, GremioResponseDTO, ProductorResponseDTO, CrearGremioDTO, RegistrarProductorEnGremioDTO
from application.mapper import productorDTO_a_productor, productorDTO_a_productor_admin
from application.usuario_service import registrar_usuario, eliminar_usuario_por_email

class ProductorService:
    def __init__(self, productor_repo: IProductorRepository, gremio_repo: IGremioRepository):        
        self.productor_repo = productor_repo
        self.gremio_repo = gremio_repo
    # Métodos del servicio
    async def crear_productor(self, productorDTO: RegistrarProductorEnGremioDTO ) -> ProductorResponseDTO:
        """Función para registrar productor (Caso de uso asociado al registro de productores en un gremio, esta acción es llevada a cabo por el admin del gremio)        """                
        #Extraer datos del DTO
        usuario = productorDTO.usuario
        productor = productorDTO_a_productor(productorDTO)
        # Validaciones de negocio        
        faltantes = [f for f in ("nombres", "apellidos") if not getattr(productor, f, None)]
        if faltantes:
            raise ValueError(f"Campos obligatorios faltantes: {', '.join(faltantes)}")
        if await self.productor_repo.es_codigo_existente(productor.codigo):
            raise ValueError("El código del productor ya existe")        
        if productor.id_gremio is not None:
            gremio = await self.gremio_repo.obtener_gremio_por_id(productor.id_gremio)
            if not gremio:
                raise ValueError("El gremio asociado no existe")
        response = registrar_usuario(usuario)
        print(response)
        if response.get("status") == "success":
            try:
                productor.u_id = response.get("data").get("u_id")
                productor.id = await self.productor_repo.agregar_productor(productor)
            except Exception as e:
                #Se envia petición para eliminar el usuario creado
                #eliminar_usuario_por_email(usuario.email)
                raise ValueError("Error insertando el productor",e)
            return ProductorResponseDTO.model_validate(productor,from_attributes=True)
        else:
            raise ValueError("Error registrando el usuario asociado al productor")
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
    async def crear_admin(self, adminDTO: CrearProductorDTO) -> ProductorResponseDTO:
        """Función para registrar productor administrador (Caso de uso asociado al registro de productores administradores del sistema, esta acción es llevada a cabo por el microservicio de usuarios)        """
        productor = productorDTO_a_productor_admin(adminDTO)
        # Validaciones de negocio        
        faltantes = [f for f in ("nombres", "apellidos") if not getattr(productor, f, None)]
        if faltantes:
            raise ValueError(f"Campos obligatorios faltantes: {', '.join(faltantes)}")              
        productor.id = await self.productor_repo.agregar_productor(productor)        
        return ProductorResponseDTO.model_validate(productor,from_attributes=True)
class GremioService:    
    def __init__(self, gremio_repo: IGremioRepository, productor_repo: IProductorRepository):
        self.gremio_repo = gremio_repo
        self.productor_repo = productor_repo
    # Métodos del servicio
    async def crear_gremio(self, id_admin:int, gremio:CrearGremioDTO) -> GremioResponseDTO:
        # Validaciones de negocio
        if not id_admin or not gremio.nombre:
            raise ValueError("Todos los campos son obligatorios")
        
        try:
            admin = await self.productor_repo.obtener_productor_por_id(id_admin)
            gremio = admin.crear_gremio(gremio.nombre)            
            id_gremio = await self.gremio_repo.agregar_gremio(gremio)
            gremio.id = id_gremio
            admin.id_gremio = id_gremio            
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
    