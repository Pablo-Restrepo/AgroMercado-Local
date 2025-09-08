from sqlmodel import SQLModel, create_engine
from ..schemas.producto import Producto
from ..schemas.cliente import Cliente
from sqlmodel import Session
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    SQLModel.metadata.create_all(engine)

def seed_data(db: Session):
    # Solo inicializa si no hay productos/clientes
    if not db.query(Producto).first():
        productos = [
            Producto(nombre="Manzana", precio=1.2),
            Producto(nombre="Banano", precio=0.8),
            Producto(nombre="Papa", precio=0.5)
        ]
        for producto in productos:
            db.add(producto)
    if not db.query(Cliente).first():
        clientes = [
            Cliente(cedula="123456", nombre="Ana", apellido="Gomez", direccion="Calle 1"),
            Cliente(cedula="654321", nombre="Luis", apellido="Perez", direccion="Calle 2")
        ]
        for cliente in clientes:
            db.add(cliente)
    db.commit()