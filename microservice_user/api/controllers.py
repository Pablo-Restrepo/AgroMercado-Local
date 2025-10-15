from fastapi import APIRouter, HTTPException, Depends
from microservice_user.api.schemas import UsuarioRegistro, UsuarioLogin, UsuarioLoginResponse
from microservice_user.application.mapper import usuario_registro_to_persona, usuario_registro_to_usuario
from microservice_user.application.services import UsuarioService

router = APIRouter()


def get_usuario_service():
    from microservice_user.api.main import usuario_service
    return usuario_service


@router.post(
    "/usuarios/registro",
    summary="Registrar un nuevo usuario y persona",
    description="""
Registra un usuario junto con su información personal.
- El email debe ser único.
- La contraseña debe tener al menos 8 caracteres.
- Todos los campos de persona son obligatorios.
""",
    response_model=dict,
    responses={
        200: {"description": "Usuario y persona registrados exitosamente"},
        400: {"description": "Error de validación o email duplicado"}
    }
)
def registrar_usuario(usuario_data: UsuarioRegistro,
                      usuario_service: UsuarioService = Depends(get_usuario_service)):
    try:
        persona = usuario_registro_to_persona(usuario_data)
        usuario = usuario_registro_to_usuario(usuario_data)
        usuario_service.registrar_usuario_y_persona(persona, usuario)
        return {"mensaje": "Usuario y persona registrados exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/usuarios/login",
    summary="Validar credenciales de usuario",
    description="""
Valida las credenciales del usuario y retorna información básica si son correctas.
- Requiere email y contraseña
- Solo usuarios activos pueden iniciar sesión
""",
    response_model=UsuarioLoginResponse,
    responses={
        200: {"description": "Credenciales válidas"},
        401: {"description": "Credenciales inválidas"}
    }
)
def login_usuario(credentials: UsuarioLogin,
                  usuario_service: UsuarioService = Depends(get_usuario_service)):
    try:
        usuario = usuario_service.validar_credenciales(
            credentials.u_email,
            credentials.u_contrasenia
        )

        if usuario:
            return UsuarioLoginResponse(
                u_id=usuario['u_id'],
                u_nombre_usuario=usuario['u_nombre_usuario'],
                u_email=usuario['u_email'],
                mensaje="Login exitoso"
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Email o contraseña incorrectos"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor" + str(e)
        )
