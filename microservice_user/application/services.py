import httpx
from domain.usuario import Usuario
from domain.persona import Persona
from domain.repositories import IUsuarioRepository, IPersonaRepository
from core.jwt_config import JWTManager


class UsuarioService:
    """
    Servicio de aplicación para casos de uso relacionados con usuarios.
    Coordina las operaciones entre entidades de dominio y repositorios.
    """

    def __init__(self, usuario_repository: IUsuarioRepository, persona_repository: IPersonaRepository):
        self.usuario_repository = usuario_repository
        self.persona_repository = persona_repository
        self.jwt_manager = JWTManager()

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

    def validar_credenciales(self, email: str, password: str):
        """Valida las credenciales del usuario y genera tokens JWT"""
        result = self.usuario_repository.find_by_email_and_password(
            email, password)

        if result:
            u_id, u_nombre_usuario, u_email, u_rol = result

            token_data = {
                'sub': str(u_id),
                'email': u_email,
                'username': u_nombre_usuario,
                'rol': u_rol
            }

            access_token = self.jwt_manager.create_access_token(
                data=token_data)
            refresh_token = self.jwt_manager.create_refresh_token(
                data=token_data)

            return {
                'u_id': u_id,
                'u_nombre_usuario': u_nombre_usuario,
                'u_email': u_email,
                'u_rol': u_rol,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return None

    def refresh_access_token(self, refresh_token: str):
        """Genera un nuevo access token usando el refresh token"""
        payload = self.jwt_manager.verify_token(refresh_token)

        if not payload or payload.get('type') != 'refresh':
            raise ValueError("Token de renovación inválido")

        # Crear nuevo access token
        token_data = {
            'sub': payload.get('sub'),
            'email': payload.get('email'),
            'username': payload.get('username')
        }

        access_token = self.jwt_manager.create_access_token(data=token_data)
        return access_token


class AuthService:
    def __init__(self):
        self.microservice_url = "http://localhost:8001"  # URL del microservicio

    async def validate_user_credentials(self, email: str, password: str) -> dict[str, any] | None:
        """Valida credenciales contra el microservicio de usuarios"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.microservice_url}/usuarios/login",
                    json={"u_email": email, "u_contrasenia": password}
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    return None
                else:
                    response.raise_for_status()

            except httpx.RequestError:
                raise Exception(
                    "Error conectando con el servicio de autenticación")

    async def register_user(self, user_data: dict[str, any]) -> dict[str, any] | None:
        """Registra un nuevo usuario en el microservicio"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.microservice_url}/usuarios/registro",
                    json=user_data
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    error_detail = response.json().get("detail", "Error desconocido")
                    raise Exception(f"Error en registro: {error_detail}")

            except httpx.RequestError:
                raise Exception("Error conectando con el servicio de usuarios")

        
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