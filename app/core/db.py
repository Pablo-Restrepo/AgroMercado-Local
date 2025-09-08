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
            Producto(nombre="Manzana", precio=1200),
            Producto(nombre="Banano", precio=800),
            Producto(nombre="Papa", precio=500),
            Producto(nombre="Tomate", precio=1000),
            Producto(nombre="Lechuga", precio=700),
            Producto(nombre="Zanahoria", precio=600),
            Producto(nombre="Cebolla", precio=900),
            Producto(nombre="Aguacate", precio=2000),
            Producto(nombre="Naranja", precio=1100),
            Producto(nombre="Limón", precio=4000),
            Producto(nombre="Pera", precio=1300),
            Producto(nombre="Sandía", precio=3000),
            Producto(nombre="Melón", precio=2500),
            Producto(nombre="Fresa", precio=2200),
            Producto(nombre="Uva", precio=2800)
        ]
        for producto in productos:
            db.add(producto)
    if not db.query(Cliente).first():
        clientes = [
            Cliente(cedula="100001", nombre="Ana", apellido="Gomez", direccion="Calle 1"),
            Cliente(cedula="100002", nombre="Luis", apellido="Perez", direccion="Calle 2"),
            Cliente(cedula="100003", nombre="Maria", apellido="Lopez", direccion="Calle 3"),
            Cliente(cedula="100004", nombre="Carlos", apellido="Ramirez", direccion="Calle 4"),
            Cliente(cedula="100005", nombre="Sofia", apellido="Torres", direccion="Calle 5")
        ]
        for cliente in clientes:
            db.add(cliente) 
    db.commit()