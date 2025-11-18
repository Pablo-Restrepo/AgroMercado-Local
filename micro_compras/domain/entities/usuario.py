class Usuario:
    def __init__(self, id: int, nombre: str, email: str, es_activo:bool = True):
        self.id = id
        self.nombre = nombre        
        self.email = email
        self.es_activo = es_activo
    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', es_activo={self.es_activo})"