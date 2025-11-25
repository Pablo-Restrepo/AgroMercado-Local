from abc import ABC, abstractmethod
from typing import List, Optional

from api.esquemas import CategoriaConsulta, ProductoConsulta
from infrastructure.mongo_collections import Categoria

class IProductoQueryRepository(ABC):
    @abstractmethod    
    def list_productos_por_gremio(self,prod_cod_gremio:int) -> List[ProductoConsulta]:
        pass
    @abstractmethod 
    def list_productos_por_productor(self,prod_id:int) -> List[ProductoConsulta]:
        pass

    @abstractmethod 
    def list_all_productos_por_categoria(self,cat_id:int) -> List[ProductoConsulta]:
        pass
    @abstractmethod
    def get_producto_por_id(self,p_id:int) -> Optional[ProductoConsulta]:
        pass

    @abstractmethod
    def list_all_productos(self) -> List[ProductoConsulta]:
        pass


    @abstractmethod
    def list_all_productos_medicinales(self) -> List[ProductoConsulta]:
        pass

    @abstractmethod    
    def list_all_productos_por_categoria(self,cat_id:int) -> List[ProductoConsulta]:
        pass

    @abstractmethod
    def list_productos_por_categoria_gremio(self,gre_id:int,cat_id:int) -> List[ProductoConsulta]:
        pass
   
    @abstractmethod
    def list_productos_por_categoria_productor(self,prod_id:int,cat_id:int) -> List[ProductoConsulta]:
        pass
    
    
    @abstractmethod
    def list_productos_medicinales_gremio(self, gre_id:int)  -> List[ProductoConsulta]:
        pass
    
    @abstractmethod
    def list_productos_medicinales_productor(self, prod_id:int)  -> List[ProductoConsulta]:
        pass
