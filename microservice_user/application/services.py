# filepath: microservice-user/application/services.py
from microservice_user.domain.usuario import Usuario

class UsuarioService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def registrar_usuario(self, usuario: Usuario):
        if self.usuario_repository.exists_email(usuario.u_email):
            raise ValueError("El email ya está registrado")
        # Aquí guardarías el usuario
        self.usuario_repository.save(usuario)