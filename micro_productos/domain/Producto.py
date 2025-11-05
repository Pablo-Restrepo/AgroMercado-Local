from .Tipo_producto import TipoProducto
from .Unidades import Unidad
from .Productor import Productor

class Producto: 
    def __init__(self, p_nombre:str, p_tipo:TipoProducto, p_unidad:Unidad, productor: Productor, p_precio:float ):
        self.p_nombre = p_nombre
        self.p_tipo = p_tipo
        self.p_unidad = p_unidad
        self.productor = productor
        self.p_precio = p_precio