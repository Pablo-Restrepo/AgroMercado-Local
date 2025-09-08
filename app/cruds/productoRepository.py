from sqlalchemy.orm import Session
from ..schemas.producto import Producto

class ProductoRepository:
    def get_producto(db: Session, producto_id: int):
        return db.query(Producto).filter(Producto.id == producto_id).first()

    def get_productos(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Producto).offset(skip).limit(limit).all()

    def create_producto(db: Session, producto: Producto):
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    def update_producto(db: Session, producto_id: int, producto_data):
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if producto:
            for key, value in producto_data.items():
                setattr(producto, key, value)
            db.commit()
            db.refresh(producto)
        return producto

    def delete_producto(db: Session, producto_id: int):
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if producto:
            db.delete(producto)
            db.commit()
        return producto

    def get_producto_por_nombre(db: Session, nombre: str):
        return db.query(Producto).filter(Producto.nombre.ilike(f"%{nombre}%")).first()