from microservice_user.domain.usuario import Usuario
from microservice_user.domain.persona import Persona
from microservice_user.domain.repositories import IUsuarioRepository, IPersonaRepository

class UsuarioService:
    """
    Servicio de aplicación para casos de uso relacionados con usuarios.
    Coordina las operaciones entre entidades de dominio y repositorios.
    """
    
    def __init__(self, usuario_repository: IUsuarioRepository, persona_repository: IPersonaRepository):
        self.usuario_repository = usuario_repository
        self.persona_repository = persona_repository

    def registrar_usuario_y_persona(self, persona: Persona, usuario: Usuario):
        """
        Caso de uso: Registrar un nuevo usuario junto con su información personal.
        
        Args:
            persona (Persona): Datos personales del usuario
            usuario (Usuario): Datos de acceso del usuario
            
        Raises:
            ValueError: Si el email ya está registrado o hay errores de validación
        """
        # Validaciones de dominio ya ejecutadas en los constructores
        if self.usuario_repository.exists_email(usuario.u_email):
            raise ValueError("El email ya está registrado")
        # Validar si la cedula ya esta registrada
        if self.persona_repository.exists_cedula(persona.p_cedula):
            raise ValueError("La cédula ya está registrada")
        # Guardar persona primero para obtener el ID
        p_id = self.persona_repository.save_persona(persona)
        
        # Asignar el ID de persona al usuario
        usuario.p_id = p_id
        
        # Guardar usuario
        self.usuario_repository.save(usuario)
        
    def eliminar_usuario_y_persona(self, usuario_id: int):
        """
        Elimina un usuario y su persona asociada.
        - Busca usuario por id
        - Elimina usuario
        - Si existe persona asociada la elimina
        """
        # Buscar usuario existente
        usuario_existente = self.usuario_repository.find_by_id(usuario_id)
        if not usuario_existente:
            raise ValueError(f"Usuario con id {usuario_id} no encontrado")

        # obtener p_id antes de eliminar usuario
        p_id = getattr(usuario_existente, "p_id", None)

        # Eliminar usuario primero
        self.usuario_repository.delete_usuario(usuario_id)

        # Si existe persona asociada, eliminarla
        if p_id:
            try:
                self.persona_repository.delete_persona(p_id)
            except ValueError:
                # si no existe persona, ignorar o loggear — aquí ignoro
                pass