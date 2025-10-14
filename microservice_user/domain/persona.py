# Define una clase con un p_id int, p_cedula, p_apellido, p_nombre str
class Persona():
    def __init__(self, p_id: int, p_cedula: str, p_apellido: str, 
                    p_nombre: str, p_fecha_nacimiento: str, p_direccion: str):
        self.p_id = p_id
        self.p_cedula = p_cedula
        self.p_apellido = p_apellido
        self.p_nombre = p_nombre 
        self.p_fecha_nacimiento = p_fecha_nacimiento
        self.p_direccion = p_direccion