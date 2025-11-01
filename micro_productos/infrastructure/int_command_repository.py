from abc import ABC, abstractmethod
from api.esquemas import ProductoRegistro, ProductoActualizacion
from domain import Productor
from domain.Producto import Producto

class IProductoCommandRepository(ABC):
    @abstractmethod
    def save_producto(producto:ProductoRegistro)-> int:
        pass

    @abstractmethod
    def edit_producto(p_id:int, Producto:ProductoActualizacion)-> int:
        pass

    @abstractmethod
    def delete_producto(p_id:int)-> int:
        pass

    @abstractmethod
    def get_productor(prod_id:int)-> Productor:
        pass

   