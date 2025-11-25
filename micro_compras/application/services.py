from application.dtos import CompraRequestDTO, HttpResponse, ProductoDTO, UsuarioDTO
from domain.entities.compra import Compra
from domain.entities.envio import Envio
from domain.entities.producto_unitario import ProductoUnitario
from domain.entities.usuario import Usuario
from domain.exceptions import *
from domain.repository import ICompraRepository, IEnvioRepository, IProductoRepository, IUsuarioRepository
from infraestructure.logging import logger
from domain.entities.producto import Producto
from infraestructure.broker.publisher_rabbitmq import publish_stock_updates

class CompraService:
    def __init__(self, compra_repository:ICompraRepository,usuario_repository:IUsuarioRepository,producto_repository:IProductoRepository):
        self.compra_repository = compra_repository
        self.usuario_repository = usuario_repository
        self.producto_repository = producto_repository

    async def create_compra(self, compra_data:CompraRequestDTO):
        """Crea una nueva compra en el sistema."""
        usuario = await self.usuario_repository.get_usuario_by_id(compra_data.id_usuario)
        if not usuario:
            logger.error(f"Usuario con ID {compra_data.id_usuario} no existe")
            raise DomainError(f"Usuario con ID {compra_data.id_usuario} no existe", code="USER_NOT_FOUND", status_code=404)        
        if not usuario.es_activo:
            logger.error(f"Usuario con ID {compra_data.id_usuario} no está activo")
            raise DomainError(f"Usuario con ID {compra_data.id_usuario} no está activo", code="USER_NOT_ACTIVE", status_code=403)
        if not compra_data.productos:
            logger.error("La lista de productos no puede estar vacía")
            raise DomainError("La lista de productos no puede estar vacía", code="EMPTY_PRODUCTS", status_code=400)
        # Crear los productos unitarios de la compra
        productos_unitarios = []
        for producto_unitario_dto in compra_data.productos:
            producto = await self.producto_repository.get_producto_by_id(producto_unitario_dto.id_producto)
            if not producto:
                logger.error(f"Producto con ID {producto_unitario_dto.id_producto} no existe")
                raise DomainError(f"Producto con ID {producto_unitario_dto.id_producto} no existe", code="PRODUCT_NOT_FOUND", status_code=404)
            if producto.stock < producto_unitario_dto.cantidad:
                logger.error(f"Stock insuficiente para el producto ID {producto_unitario_dto.id_producto}")
                raise DomainError(f"Stock insuficiente para el producto ID {producto_unitario_dto.id_producto}", code="INSUFFICIENT_STOCK", status_code=400)
            productos_unitarios.append(ProductoUnitario(
                id_producto=producto_unitario_dto.id_producto,
                cantidad=producto_unitario_dto.cantidad,
                precio_unitario=producto.precio,
                unidad=producto.unidad
            ))
        compra = Compra(
            id_usuario=compra_data.id_usuario,
            productos=productos_unitarios
        )
        logger.info(f"Creando compra para usuario ID {compra_data.id_usuario} con {len(compra.productos)} productos")
        compra.calcular_total()
        saved_compra = await self.compra_repository.save_compra(compra)
        #Después de crear la compra, debe enviarse un mensaje de actualización sobre el stock para el micro de productos
        publish_stock_updates(productos_unitarios)
        return HttpResponse(
            status_code=201,
            content={"message": "Compra creada exitosamente", "compra_id": saved_compra.id}
        )
    async def confirmar_compra(self, compra_id):
        compra = await self.compra_repository.get_compra_by_id(compra_id)
        if not compra:
            logger.error(f"Compra con ID {compra_id} no encontrada")
            raise DomainError(f"Compra con ID {compra_id} no encontrada", code="COMPRA_NOT_FOUND", status_code=404)                
        try:
            compra.confirmar_compra()            
        except Exception as e:
            raise DomainError(str(e), code="COMPRA_CONFIRMATION_FAILED", status_code=400)
        await self.compra_repository.update_compra(compra)
        return HttpResponse(
            status_code=200,
            content={"message": "Compra confirmada exitosamente", "compra_id": compra.id}
        )
    async def pagar_compra(self, compra_id:int, destino:str, envio_service:'EnvioService'):
        compra = await self.compra_repository.get_compra_by_id(compra_id)
        if not compra:
            logger.error(f"Compra con ID {compra_id} no encontrada")
            raise DomainError(f"Compra con ID {compra_id} no encontrada", code="COMPRA_NOT_FOUND", status_code=404)                
        try:
            compra.pagar_compra()
        except Exception as e:
            raise DomainError(str(e), code="COMPRA_PAYMENT_FAILED", status_code=400)
        await self.compra_repository.update_compra(compra)
        #Se generan los envios asociados a la compra
        await envio_service.generar_envios(compra,destino)
        return HttpResponse(
            status_code=200,
            content={"message": "Compra pagada exitosamente", "compra_id": compra.id}
        )

    async def get_compra(self, compra_id):
        """Obtiene una compra por su ID."""        
        compra = await self.compra_repository.get_compra_by_id(compra_id) 
        if not compra:
            logger.error(f"Compra con ID {compra_id} no encontrada")
            raise DomainError(f"Compra con ID {compra_id} no encontrada", code="COMPRA_NOT_FOUND", status_code=404)                
        return HttpResponse(
            status_code=200,
            content=compra.to_dict()
        )
    async def get_compras_by_usuario(self, usuario_id):
        """Obtiene todas las compras de un usuario por su ID."""
        usuario = await self.usuario_repository.get_usuario_by_id(usuario_id)
        if not usuario:
            logger.error(f"Usuario con ID {usuario_id} no existe")
            raise DomainError(f"Usuario con ID {usuario_id} no existe", code="USER_NOT_FOUND", status_code=404)
        compras = await self.compra_repository.get_compras_by_usuario(usuario_id) 
        compras_list = [compra.to_dict() for compra in compras]
        return HttpResponse(
            status_code=200,
            content={"compras": compras_list}
        )
    def update_compra(self, compra_id, compra_data):
        #TODO lógica para actualizar una compra
        return self.compra_repository.update(compra_id, compra_data)

    def delete_compra(self, compra_id):
        #TODO lógica para eliminar una compra
        return self.compra_repository.delete(compra_id)
class UsuarioService:
    def __init__(self, usuario_repository:IUsuarioRepository):
        self.usuario_repository = usuario_repository

    async def crear_usuario(self, usuario_data:UsuarioDTO):                
        usuario_entity = Usuario(
            id=usuario_data.id,
            nombre=usuario_data.nombre,
            email=usuario_data.email,
            es_activo=usuario_data.es_activo
        )
        return await self.usuario_repository.save_usuario(usuario_entity)
class ProductoService:
    def __init__(self, producto_repository:IProductoRepository):
        self.producto_repository = producto_repository

    async def crear_producto(self, producto_data:ProductoDTO):                
        producto_entity = Producto(
            id=producto_data.id,
            nombre=producto_data.nombre,
            id_gremio=producto_data.id_gremio, 
            precio=producto_data.precio,
            unidad=producto_data.unidad,
            stock=producto_data.stock            
        )
        return await self.producto_repository.save_producto(producto_entity)
class EnvioService:
    def __init__(self, envio_repository:IEnvioRepository, producto_repository:IProductoRepository):
        self.envio_repository = envio_repository    
        self.producto_repository = producto_repository

    async def generar_envios(self, compra:Compra, destino:str):
        """Genera los envios asociados a una compra dependiendo del gremio de cada producto."""
        #Agrupar productos por gremio
        envios_dict = {}
        for producto_unitario in compra.productos:
            producto = await self.producto_repository.get_producto_by_id(producto_unitario.id_producto)
            if not producto:
                logger.error(f"Producto con ID {producto_unitario.id_producto} no encontrado para generar envio")
                raise DomainError(f"Producto con ID {producto_unitario.id_producto} no encontrado para generar envio", code="PRODUCT_NOT_FOUND", status_code=404)                
            id_gremio = producto.id_gremio
            if id_gremio not in envios_dict:
                envios_dict[id_gremio] = {
                    "productos": [],
                    "valor_total": 0
                }
            envios_dict[id_gremio]["productos"].append(producto_unitario)
            envios_dict[id_gremio]["valor_total"] += producto_unitario.cantidad * producto_unitario.precio_unitario
        #Crear envios por gremio
        for id_gremio, envio_info in envios_dict.items():
            # Se crea una compra por gremio
            compra_gremio = Compra(id=compra.id, id_usuario=compra.id_usuario, productos=envio_info["productos"],fecha=compra.fecha, total=envio_info["valor_total"], estado=compra.estado)
            envio = Envio(
                id_gremio=id_gremio,
                compra=compra_gremio,
                destino=destino                
            )
            await self.envio_repository.save_envio(envio)
        logger.info(f"Se generaron {len(envios_dict)} envíos para la compra ID {compra.id}")
    async def update_envio_status(self, envio_id:int, nuevo_estado:str):
        envio = await self.envio_repository.get_envio_by_id(envio_id)
        if not envio:
            logger.error(f"Envío con ID {envio_id} no encontrado")
            raise DomainError(f"Envío con ID {envio_id} no encontrado", code="ENVIO_NOT_FOUND", status_code=404)                
        try:
            nuevo_estado = nuevo_estado.lower()
            if nuevo_estado == "despachado":
                envio.despachar_envio()
            elif nuevo_estado == "en_ruta":
                envio.enviar_en_ruta()
            elif nuevo_estado == "entregado":
                envio.entregar_envio()
            else:
                logger.error(f"Estado inválido: {nuevo_estado}")
                raise DomainError(f"Estado inválido: {nuevo_estado}", code="INVALID_STATUS", status_code=400)                
        except Exception as e:
            raise DomainError(str(e), code="ENVIO_STATUS_UPDATE_FAILED", status_code=400)
        await self.envio_repository.update_envio(envio)
        return HttpResponse(
            status_code=200,
            content={"message": "Estado de envío actualizado exitosamente", "envio_id": envio.id}
        )
    async def get_envios_por_gremio(self, id_gremio:int):
        envios = await self.envio_repository.get_envios_by_id_gremio(id_gremio)
        envios_list = [envio.to_dict() for envio in envios]
        return HttpResponse(
            status_code=200,
            content={"envios": envios_list}
        )
    async def get_envios_por_usuario(self, id_usuario:int):
        envios = await self.envio_repository.get_envios_by_usuario(id_usuario)
        envios_list = [envio.to_dict() for envio in envios]
        return HttpResponse(
            status_code=200,
            content={"envios": envios_list}
        )