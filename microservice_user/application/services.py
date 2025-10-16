import httpx
from typing import Optional, Dict, Any
from microservice_user.domain.usuario import Usuario
from microservice_user.domain.persona import Persona
from microservice_user.infrastructure.db import UsuarioRepository, PersonaRepository
from microservice_user.core.jwt_config import JWTManager


class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository, persona_repository: PersonaRepository):
        self.usuario_repository = usuario_repository
        self.persona_repository = persona_repository
        self.jwt_manager = JWTManager()

    def registrar_usuario_y_persona(self, persona: Persona, usuario: Usuario):
        # Validaciones de dominio ya ejecutadas en los constructores
        if self.usuario_repository.exists_email(usuario.u_email):
            raise ValueError("El email ya está registrado")
        p_id = self.persona_repository.save_persona(persona)
        usuario.p_id = p_id
        self.usuario_repository.save(usuario)

    def validar_credenciales(self, email: str, password: str):
        """Valida las credenciales del usuario y genera tokens JWT"""
        result = self.usuario_repository.find_by_email_and_password(
            email, password)
        if result:
            u_id, u_nombre_usuario, u_email, u_es_activo = result

            # Datos para el token
            token_data = {
                'sub': str(u_id),
                'email': u_email,
                'username': u_nombre_usuario
            }

            # Generar tokens
            access_token = self.jwt_manager.create_access_token(
                data=token_data)
            refresh_token = self.jwt_manager.create_refresh_token(
                data=token_data)

            return {
                'u_id': u_id,
                'u_nombre_usuario': u_nombre_usuario,
                'u_email': u_email,
                'u_es_activo': u_es_activo,
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

    async def validate_user_credentials(self, email: str, password: str) -> Optional[Dict[str, Any]]:
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

    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
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
