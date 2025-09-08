from sqlalchemy.orm import Session
from ..models.producto import Producto
from ..cruds.productoRepository import ProductoRepository

class ProductoService:
    @staticmethod
    def obtener_producto(db: Session, producto_id: int):
        return ProductoRepository.get_producto(db, producto_id)

    @staticmethod
    def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
        return ProductoRepository.get_productos(db, skip, limit)

    @staticmethod
    def crear_producto(db: Session, producto: Producto):
        return ProductoRepository.create_producto(db, producto)

    @staticmethod
    def actualizar_producto(db: Session, producto_id: int, producto_data):
        return ProductoRepository.update_producto(db, producto_id, producto_data)

    @staticmethod
    def eliminar_producto(db: Session, producto_id: int):
        return ProductoRepository.delete_producto(db, producto_id)

    @staticmethod
    def obtener_producto_por_nombre(db: Session, nombre: str):
        return ProductoRepository.get_producto_por_nombre(db, nombre)