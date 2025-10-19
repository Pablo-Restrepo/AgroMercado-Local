# Esta es una interfaz de repositorio para manejar la persistencia de datos.
from abc import ABC, abstractmethod
from typing import List
from domain.models import Productor, Gremio

#Interface para el repositorio de gremios
class IGremioRepository(ABC):
    @abstractmethod
    def agregar_gremio(self, gremio: Gremio):
        pass
    @abstractmethod
    def obtener_gremios(self) -> List[Gremio]:
        pass
    @abstractmethod
    def obtener_gremio_por_id(self, id) -> Gremio:
        pass
    @abstractmethod
    def obtener_productores_por_gremio(self, id_gremio) -> List[Productor]:
        pass

#Interface para el repositorio de productores
class IProductorRepository(ABC):
    @abstractmethod
    def agregar_productor(self, productor: Productor):
        pass
    @abstractmethod
    def obtener_productores(self) -> List[Productor]:
        pass
    @abstractmethod
    def obtener_productor_por_id(self, id) -> Productor:
        pass
    @abstractmethod
    def actualizar_productor(self, productor: Productor):
        pass
    @abstractmethod
    def eliminar_productor(self, id):
        pass
    @abstractmethod
    def es_codigo_existente(self, codigo: str) -> bool:
        pass