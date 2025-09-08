from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select
from uuid import UUID
from ..schemas.pedido import Pedido
from ..schemas.producto_unitario import ProductoUnitario

class PedidoRepository:
    def get_pedido(db: Session, pedido_id: UUID):
        return (
            db.exec(
                select(Pedido)
                .where(Pedido.id == pedido_id)
                .options(selectinload(Pedido.productos_unitarios))
            )
            .scalars()        
            .first())

    def get_pedidos(db: Session) -> list[Pedido]:
        return (
            db.exec(
                select(Pedido)
                .options(selectinload(Pedido.productos_unitarios))
            )
            .scalars()   
            .all()       
        )

    def create_pedido(db: Session, pedido: Pedido):
        db.add(pedido)
        db.commit()
        db.refresh(pedido)
        return pedido

    def update_pedido(db: Session, pedido_id: int, pedido_data):
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        update_data = pedido_data.model_dump(exclude_unset=True)
        pedido.sqlmodel_update(update_data)

        db.add(pedido)
        db.commit()
        db.refresh(pedido)
        """
            if pedido:
                for key, value in pedido_data.items():
                    setattr(pedido, key, value)
                db.commit()
                db.refresh(pedido)
        """
        return pedido

    def delete_pedido(db: Session, pedido_id: int):
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            db.delete(pedido)
            db.commit()
        return pedido


    def get_pedidos_por_cedula(db: Session, cedula: str):
        return db.query(Pedido).join(Pedido.cliente).filter(Pedido.cliente.cedula == cedula).all()
    
    @staticmethod
    def create_producto_unitario(db: Session, producto_unitario: ProductoUnitario):
        db.add(producto_unitario)
        db.commit()
        db.refresh(producto_unitario)
        return producto_unitario

    @staticmethod
    def get_productos_unitarios_por_pedido(db: Session, pedido_id: int):
        return db.query(ProductoUnitario).filter(ProductoUnitario.pedido_id == pedido_id).all()
    
    @staticmethod
    def delete_productos_unitarios_por_pedido(db: Session, pedido_id: int):
        db.query(ProductoUnitario).filter(ProductoUnitario.pedido_id == pedido_id).delete(synchronize_session=False)
        db.commit()

