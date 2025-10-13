# Este archivo define las entidades del dominio y sus relaciones
from typing import List

class Persona:
    def __init__(self, id, nombres, apellidos):
        if not id or not nombres or not apellidos:
            raise ValueError("Todos los campos son obligatorios")
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos

class Productor(Persona):
    def __init__(self, id, codigo, nombres, apellidos, id_gremio = None, rol = None):
        super().__init__(id, nombres, apellidos)
        if not codigo:
            raise ValueError("El código es obligatorio")
        self.codigo = codigo
        self.id_gremio = id_gremio
        #Puede ser 'ADMIN','MIEMBRO' o None
        self.rol = rol
        self.es_activo = True
    #Métodos de negocio
    def eliminar_productor(self):
        self.es_activo = False
        self.id_gremio = None
        self.rol = None
    
class Gremio:
    #TO DO: Definir si es necesario que el gremio contenga una lista de productores o 
    # si es mejor tener solo sus ids
    def __init__(self, id, nombre, productores:List[Productor] = None):
        if not id or not nombre:
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
        productor.rol = 'MIEMBRO'        

    def remover_productor(self, productor:Productor):
        self.productores = [p for p in self.productores if p.id != productor.id]
        productor.id_gremio = None
        productor.rol = None

    def es_miembro(self, productor:Productor) -> bool:
        return any(p.id == productor.id for p in self.productores)
    
    def obtener_productores(self) -> List[Productor]:
        return self.productores
    
    def obtener_admin(self) -> Productor:
        for productor in self.productores:
            if productor.rol == 'ADMIN':
                return productor
        return None
