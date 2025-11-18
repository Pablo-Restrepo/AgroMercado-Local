from abc import ABC, abstractmethod
from typing import List

from domain.entities.compra import Compra
from domain.entities.envio import Envio
from domain.entities.producto import Producto
from domain.entities.producto_unitario import ProductoUnitario
from domain.entities.usuario import Usuario

#Interfaz para el repositorio de productos
class IProductoRepository(ABC):
    @abstractmethod
    async def save_producto(self, producto:Producto):
        pass
    @abstractmethod
    async def get_productos(self)-> List[Producto]:
        pass
    @abstractmethod
    async def get_producto_by_id(self, id:int)-> Producto:
        pass
class IProductoUnitarioRepository(ABC):
    @abstractmethod
    async def save_producto_unitario(self, producto_unitario:ProductoUnitario):
        pass    
    @abstractmethod
    async def get_productos_unitarios_by_compra(self, id_compra:int) -> List[ProductoUnitario]:
        pass
class ICompraRepository(ABC):
    @abstractmethod
    def save_compra(self, compra:Compra)-> Compra:
        pass
    @abstractmethod
    def get_compras(self) -> List[Compra]:
        pass
    @abstractmethod
    def get_compra_by_id(self, id:int)-> Compra:
        pass
    @abstractmethod
    def get_compras_by_usuario(self, id_usuario:int):
        pass
    @abstractmethod
    def update_compra(self, compra:Compra):
        pass
class IUsuarioRepository(ABC):
    @abstractmethod
    def save_usuario(self, usuario:Usuario):
        pass   
    @abstractmethod
    def get_usuario_by_id(self, id:int)-> Usuario:
        pass
    @abstractmethod
    def get_usuario_by_email(self, email:str  )-> Usuario:
        pass    
class IEnvioRepository(ABC):
    @abstractmethod
    def save_envio(self, envio:Envio):
        pass    
    @abstractmethod
    def get_envio_by_id(self, id:int):
        pass    
    @abstractmethod
    def update_envio(self, envio:Envio):
        pass            