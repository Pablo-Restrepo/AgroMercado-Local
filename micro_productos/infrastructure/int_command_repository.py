from abc import ABC, abstractmethod
from api.esquemas import ProductoRegistro, ProductoActualizacion, ProductorConsulta

from abc import ABC, abstractmethod

class IProductoCommandRepository(ABC):

    @abstractmethod
    async def save_producto(self, producto: ProductoRegistro) -> int:
        pass

    @abstractmethod
    async def edit_producto(self, p_id: int, producto: ProductoActualizacion) -> int:
        pass

    @abstractmethod
    async def delete_producto(self, p_id: int) -> int:
        pass

    @abstractmethod
    async def get_productor(self, prod_id: int) -> ProductorConsulta:
        pass


   