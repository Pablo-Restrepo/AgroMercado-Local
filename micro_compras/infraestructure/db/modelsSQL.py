from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class ProductoModel(SQLModel, table=True):
    __tablename__="producto"
    p_id: Optional[int] = Field(default=None, primary_key=True)
    p_nombre: str = Field(max_length=100)
    p_id_gremio: int = Field(default=None)
    p_precio: float = Field(default=None)
    p_unidad: str = Field(max_length=50)
    p_stock: int = Field(default=None)

class CompraModel(SQLModel, table=True):
    __tablename__="compra"
    c_id: Optional[int] = Field(default=None, primary_key=True)
    u_id: Optional[int] = Field(foreign_key="usuario.u_id")
    c_productos: List["ProductoUnitarioModel"] = Relationship(back_populates="pu_compra")
    c_envio: Optional["EnvioModel"] = Relationship(back_populates="e_compra")
    c_fecha: datetime = Field(default=None)
    c_total: float = Field(default=None)
    c_estado: str = Field(max_length=50)

class ProductoUnitarioModel(SQLModel, table=True):
    __tablename__="producto_unitario"
    pu_id: Optional[int] = Field(default=None, primary_key=True)
    p_id: Optional[int] = Field(foreign_key="producto.p_id")
    c_id: Optional[int] = Field(default=None, foreign_key="compra.c_id")  # FK hacia compra
    pu_cantidad: int = Field(default=None)
    pu_precio_unitario: int = Field(default=None)
    pu_unidad: str = Field(max_length=50)
    pu_subtotal: float = Field(default=None)
    # Relacion con producto (unidireccional: no back_populates)
    pu_producto: Optional[ProductoModel] = Relationship()
    # Relacion con compra (bidireccional; nombre coincide con CompraModel.c_productos)
    pu_compra: Optional[CompraModel] = Relationship(back_populates="c_productos")    

class EnvioModel(SQLModel, table=True):
    __tablename__="envio"
    e_id: Optional[int] = Field(default=None, primary_key=True)
    e_destino: str = Field(max_length=200)
    e_valor: float = Field(default=None)    
    e_estado: str = Field(max_length=50)
    e_fecha_envio: datetime = Field(default=None)        
    e_c_id: Optional[int] = Field(default=None, foreign_key="compra.c_id")
    e_compra :Optional[CompraModel] = Relationship(back_populates="c_envio")
class UsuarioModel(SQLModel, table=True):
    __tablename__="usuario"
    u_id: Optional[int] = Field(default=None, primary_key=True)
    u_nombre: str = Field(max_length=100)
    u_email: str = Field(max_length=100, unique=True)
    u_es_activo: bool = Field(default=True)
    
