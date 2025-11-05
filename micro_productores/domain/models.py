# Este archivo define las entidades del dominio y sus relaciones
from typing import List

from enum import Enum

class RolEnum(str, Enum):
    PRODUCTOR_ADMIN = "productor-admin"
    PRODUCTOR_AFILIADO = "productor-afiliado"
    CLIENTE = "cliente"

class Persona:
    def __init__(self, id, nombres, apellidos):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos

class Productor(Persona):
    def __init__(self, id, codigo, nombres, apellidos, id_gremio = None, rol = None, es_activo = True,u_id: int = None):
        super().__init__(id, nombres, apellidos)        
        self.codigo = codigo
        self.id_gremio = id_gremio
        #Los roles están definidos en RolEnum
        self.rol = rol
        self.es_activo = es_activo
        self.u_id = u_id
    #Métodos de negocio
    def eliminar_productor(self):
        self.es_activo = False
        self.id_gremio = None        
    def es_activo(self) -> bool:
        return self.es_activo
    def crear_gremio(self, nombre_gremio):
        if self.rol != RolEnum.PRODUCTOR_ADMIN:
            raise ValueError("Solo un productor con rol ADMIN puede crear un gremio")
        if self.id_gremio is not None:
            raise ValueError("El productor ya pertenece a un gremio")
        gremio = Gremio(None,nombre=nombre_gremio, productores=[self])        
        return gremio

class Gremio:
    #TO DO: Definir si es necesario que el gremio contenga una lista de productores o 
    # si es mejor tener solo sus ids
    def __init__(self, id:int | None, nombre, productores:List[Productor] = None):
        if not nombre:
            raise ValueError("Todos los campos son obligatorios")
        self.id = id
        self.nombre = nombre
        self.productores = productores if productores is not None else []
        self.es_activo = True

    #Métodos de negocio    
    def agregar_productor(self, productor:Productor):
        if any(p.id == productor.id for p in self.productores):
            raise ValueError("El productor ya pertenece al gremio")
        self.productores.append(productor)
        productor.id_gremio = self.id
        productor.rol = RolEnum.PRODUCTOR_AFILIADO        

    def remover_productor(self, productor:Productor):
        self.productores = [p for p in self.productores if p.id != productor.id]
        if productor.rol == RolEnum.PRODUCTOR_ADMIN:
            raise ValueError("No se puede remover al administrador del gremio")
        productor.id_gremio = None
        productor.rol = None

    def es_miembro(self, productor:Productor) -> bool:
        return any(p.id == productor.id for p in self.productores)
    
    def obtener_productores(self) -> List[Productor]:
        return self.productores
    
    def obtener_admin(self) -> Productor:
        for productor in self.productores:
            if productor.rol == RolEnum.PRODUCTOR_ADMIN:
                return productor
        return None
