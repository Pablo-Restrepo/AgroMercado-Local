from pydantic import BaseModel

class ProductoRegistro(BaseModel):
    p_nombre: str
    p_tipo: str
    p_unidad: str
    prod_id: int
    img: str
    p_precio: float

class ProductoProductorSync():
    def __init__(self, p_nombre:str, prod_id:int,prod_nombre:str,prod_nombre_gremio:str, p_tipo:str, p_unidad:str, p_id: int , img: str, p_precio:float):
        self.p_id =p_id
        self.p_nombre = p_nombre
        self.p_tipo = p_tipo
        self.p_unidad = p_unidad
        self.prod_id = prod_id
        self.p_precio = p_precio
        self.img = img
        self.prod_id
        self.prod_nombre =prod_nombre
        self.prod_nombre_gremio = prod_nombre_gremio
        
class ProductoActualizacion(BaseModel):
    p_nombre: str
    p_tipo: str
    p_unidad: str
    img: str
    p_precio: float

class ProductoConsulta(BaseModel):
    p_nombre: str
    p_tipo: str
    p_unidad : str
    gre_nombre : str
    p_precio : float
    img : str

class ProductorRegistroConsulta(BaseModel):
    prod_id: int
    prod_nombre: str
    prod_apellido:str
    prod_cod_gremio: int
    prod_nombre_gremio: str

