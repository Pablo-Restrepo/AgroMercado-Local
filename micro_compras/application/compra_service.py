from application.dtos import CompraRequestDTO, HttpResponse
from domain.entities.compra import Compra
from domain.entities.producto_unitario import ProductoUnitario
from domain.exceptions import *
from domain.repository import ICompraRepository, IProductoRepository, IUsuarioRepository
from infraestructure.logging import logger

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
        compra.calcular_total()
        saved_compra = await self.compra_repository.save_compra(compra)
        return HttpResponse(
            status_code=201,
            content={"message": "Compra creada exitosamente", "compra_id": saved_compra.id}
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

    def update_compra(self, compra_id, compra_data):
        # Logic to update an existing compra
        return self.compra_repository.update(compra_id, compra_data)

    def delete_compra(self, compra_id):
        # Logic to delete a compra by ID
        return self.compra_repository.delete(compra_id)