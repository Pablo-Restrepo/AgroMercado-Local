from abc import ABC, abstractmethod
from typing import List, Optional

from api.esquemas import ProductoConsulta

class IProductoQueryRepository(ABC):
    @abstractmethod    
    def list_productos_por_gremio(self,prod_cod_gremio:int) -> List[ProductoConsulta]:
        pass
    @abstractmethod 
    def list_productos_por_productor(self,prod_id:int) -> List[ProductoConsulta]:
        pass
    @abstractmethod
    def get_producto_por_id(self,p_id:int) -> Optional[ProductoConsulta]:
        pass

    @abstractmethod
    def list_all_productos(self) -> List[ProductoConsulta]:
        pass
