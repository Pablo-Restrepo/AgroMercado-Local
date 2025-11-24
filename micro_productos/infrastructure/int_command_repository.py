from abc import ABC, abstractmethod
from api.esquemas import ProductoCompra, ProductoRegistro, ProductoActualizacion, ProductorRegistroConsulta

from abc import ABC, abstractmethod

class IProductoCommandRepository(ABC):

    @abstractmethod
    async def save_producto(self, producto: ProductoRegistro) -> int:
        pass

    @abstractmethod
    async def edit_producto(self, p_id: int, producto: ProductoActualizacion) -> int:
        pass

    @abstractmethod
    async def edit_producto_stock(self, p_id: int, cant:int) -> int:
        pass

    @abstractmethod
    async def delete_producto(self, p_id: int) -> int:
        pass

    @abstractmethod
    async def get_productor(self, prod_id: int) -> ProductorRegistroConsulta:
        pass

    @abstractmethod
    async def save_productor(self, productor: ProductorRegistroConsulta) -> int:
        pass

   