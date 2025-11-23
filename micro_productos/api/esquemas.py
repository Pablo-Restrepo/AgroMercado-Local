from enum import Enum
from pydantic import BaseModel, field_validator


class RolEnum(str, Enum):
    PRODUCTOR_ADMIN = "productor-admin"
    PRODUCTOR_AFILIADO = "productor-afiliado"
    CLIENTE = "cliente"
    
class ProductoRegistro(BaseModel):
    p_nombre: str
    p_tipo: str
    p_unidad: str
    prod_id: int
    img: str
    p_precio: float
    p_stock: int

    @field_validator("p_precio")
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError("p_precio debe ser mayor a 0")
        return v

    @field_validator("p_stock")
    def validar_stock(cls, v):
        if v <= 0:
            raise ValueError("p_stock debe ser mayor a 0")
        return v

class ProductoProductorSync():
    def __init__(self, p_nombre:str, prod_id:int,prod_nombre:str,prod_nombre_gremio:str, p_tipo:str, p_unidad:str, p_id: int , img: str, p_precio:float, p_stock: int):
        self.p_id =p_id
        self.p_nombre = p_nombre
        self.p_tipo = p_tipo
        self.p_unidad = p_unidad
        self.prod_id = prod_id
        self.p_precio = p_precio
        self.p_stock =p_stock
        self.img = img
        self.prod_id
        self.prod_nombre =prod_nombre
        self.prod_nombre_gremio = prod_nombre_gremio
        self.p_stock = p_stock
        
class ProductoActualizacion(BaseModel):
    p_nombre: str
    p_tipo: str
    p_unidad: str
    img: str
    p_precio: float
    p_stock: int

    @field_validator("p_precio")
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError("p_precio debe ser mayor a 0")
        return v

    @field_validator("p_stock")
    def validar_stock(cls, v):
        if v <= 0:
            raise ValueError("p_stock debe ser mayor a 0")
        return v

class ProductoConsulta(BaseModel):
    p_nombre: str
    p_tipo: str
    p_unidad : str
    gre_nombre : str
    p_precio : float
    p_stock:int
    img : str

class ProductorRegistroConsulta(BaseModel):
    prod_id: int
    prod_nombre: str
    prod_apellido:str
    prod_cod_gremio: int
    prod_nombre_gremio: str

    @field_validator("prod_id")
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError("prod_id debe ser mayor a 0")
        return v

    @field_validator("prod_cod_gremio")
    def validar_stock(cls, v):
        if v <= 0:
            raise ValueError("prod_cod_gremio debe ser mayor a 0")
        return v
    
class ProductoCompra(BaseModel):
    p_id: int
    cant: int 

    @field_validator("cant")
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError("cant debe ser mayor a 0")
        return v


