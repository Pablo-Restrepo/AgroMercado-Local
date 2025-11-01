from pydantic import BaseModel

class ProductoRegistro(BaseModel):
    def __init__(self, p_nombre:str, p_tipo:str, p_unidad:str, prod_id: int , img: str, p_precio:float):
        self.p_nombre = p_nombre
        self.p_tipo = p_tipo
        self.p_unidad = p_unidad
        self.prod_id = prod_id
        self.p_precio = p_precio
        self.img = img

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
    def __init__(self, p_nombre:str, p_tipo:str, p_unidad:str,img: str, p_precio:float):
        self.p_nombre = p_nombre
        self.p_tipo = p_tipo
        self.p_unidad = p_unidad
        self.p_precio = p_precio
        self.img = img

class ProductoConsulta():
    def __init__(self, p_nombre:str, p_tipo:str, p_unidad:str, gre_nombre:str , img: str, p_precio:float):
        self.p_nombre = p_nombre
        self.p_tipo = p_tipo
        self.p_unidad = p_unidad
        self.gre_nombre = gre_nombre
        self.p_precio = p_precio
        self.img = img