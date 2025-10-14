from microservice_user.domain.usuario import Usuario
from microservice_user.domain.persona import Persona
from microservice_user.infrastructure.db import UsuarioRepository, PersonaRepository
class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository, persona_repository: PersonaRepository):
        self.usuario_repository = usuario_repository
        self.persona_repository = persona_repository

    def registrar_usuario_y_persona(self, persona: Persona, usuario: Usuario):
        # Validaciones de dominio ya ejecutadas en los constructores
        if self.usuario_repository.exists_email(usuario.u_email):
            raise ValueError("El email ya está registrado")
        p_id = self.persona_repository.save_persona(persona)
        usuario.p_id = p_id
        self.usuario_repository.save(usuario)