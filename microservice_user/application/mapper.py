from microservice_user.api.schemas import UsuarioRegistro
from microservice_user.domain.usuario import Usuario
from microservice_user.domain.persona import Persona

def usuario_registro_to_persona(usuario_data: UsuarioRegistro) -> Persona:
    return Persona(
        p_id=None,
        p_cedula=usuario_data.persona.p_cedula,
        p_apellido=usuario_data.persona.p_apellido,
        p_nombre=usuario_data.persona.p_nombre,
        p_fecha_nacimiento=usuario_data.persona.p_fecha_nacimiento,
        p_direccion=usuario_data.persona.p_direccion,
        p_telefono=usuario_data.persona.p_telefono
    )

def usuario_registro_to_usuario(usuario_data: UsuarioRegistro) -> Usuario:
    return Usuario(
        u_id=None,
        u_nombre_usuario=usuario_data.u_nombre_usuario,
        u_contrasenia=usuario_data.u_contrasenia,
        u_email=usuario_data.u_email,
        p_id=None  # Se asignará luego
    )