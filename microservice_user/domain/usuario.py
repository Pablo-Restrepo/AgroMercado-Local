from enum import Enum


class RolEnum(str, Enum):
    PRODUCTOR_ADMIN = "productor-admin"
    PRODUCTOR_AFILIADO = "productor-afiliado"
    CLIENTE = "cliente"


class Usuario:
    def __init__(self, u_id: int, u_nombre_usuario: str, u_contrasenia: str, u_email: str, p_id: int, u_rol: RolEnum):
        self.u_id = u_id
        self.u_nombre_usuario = u_nombre_usuario
        self.u_contrasenia = u_contrasenia
        self.u_email = u_email
        self.p_id = p_id
        self.u_rol = u_rol
    
    def ejecutar_validaciones(self):
        for metodo in self._metodos_validacion():
            metodo()

    def _metodos_validacion(self):
        return [
            self.validar_contrasenia,
            self.validar_email,
            # Agrega aquí más métodos de validación si los necesitas
        ]

    def validar_contrasenia(self):
        if len(self.u_contrasenia) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

    def validar_email(self):
        if "@" not in self.u_email or "." not in self.u_email:
            raise ValueError("El email no es válido")
