# Filepath: microservice_user/domain/persona.py
class Persona:
    def __init__(self, p_id: int, p_cedula: str, p_apellido: str, 
                 p_nombre: str, p_fecha_nacimiento: str, p_direccion: str,
                 p_telefono: str):
        self.p_id = p_id
        self.p_cedula = p_cedula
        self.p_apellido = p_apellido
        self.p_nombre = p_nombre 
        self.p_fecha_nacimiento = p_fecha_nacimiento
        self.p_direccion = p_direccion
        self.p_telefono = p_telefono
        self.ejecutar_validaciones()

    def ejecutar_validaciones(self):
        if not self.p_cedula or not self.p_apellido or not self.p_nombre:
            raise ValueError("Cédula, apellido y nombre son obligatorios")