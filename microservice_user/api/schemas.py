from pydantic import BaseModel
from microservice_user.domain.usuario import RolEnum


class PersonaRegistro(BaseModel):
    p_cedula: str
    p_apellido: str
    p_nombre: str
    p_fecha_nacimiento: str
    p_direccion: str
    p_telefono: str


class UsuarioRegistro(BaseModel):
    u_nombre_usuario: str
    u_contrasenia: str
    u_email: str
    u_rol: RolEnum = RolEnum.CLIENTE
    persona: PersonaRegistro


class UsuarioLogin(BaseModel):
    u_email: str
    u_contrasenia: str


class UsuarioLoginResponse(BaseModel):
    u_id: int
    u_nombre_usuario: str
    u_email: str
    u_rol: str
    access_token: str
    refresh_token: str
    token_type: str
    mensaje: str


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
