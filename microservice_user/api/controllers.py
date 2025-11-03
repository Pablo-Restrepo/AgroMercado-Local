from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from microservice_user.api.schemas import (
    UsuarioRegistro, UsuarioLogin, UsuarioLoginResponse,
    TokenRefresh, TokenResponse
)
from microservice_user.application.mapper import usuario_registro_to_persona, usuario_registro_to_usuario
from microservice_user.application.services import UsuarioService
from microservice_user.api.response import APIResponse
from microservice_user.infrastructure.queue.queue_rabbit import publish_user_registration
from microservice_user.core.auth_middleware import get_current_user
from microservice_user.domain.usuario import RolEnum

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
    response_model=APIResponse,
    responses={
        200: {"description": "Usuario y persona registrados exitosamente"},
        400: {"description": "Error de validación o email duplicado"}
    }
)
def registrar_usuario(
    usuario_data: UsuarioRegistro,
    background_tasks: BackgroundTasks,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    try:
        persona = usuario_registro_to_persona(usuario_data)
        usuario = usuario_registro_to_usuario(usuario_data)
        usuario_service.registrar_usuario_y_persona(persona, usuario)

        # Datos que queremos en la cola (solo algunos atributos)
        data = {
            "u_id": usuario.u_id,
            "nombres": persona.p_nombre,
            "apellidos": persona.p_apellido,
            "email": usuario.u_email,
            "rol": usuario.u_rol
        }

        # Encolar publicación en background para no bloquear la respuesta
        background_tasks.add_task(publish_user_registration, data)

        return APIResponse(status="success", message="Usuario y persona registrados exitosamente", data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/usuarios/login",
    summary="Iniciar sesión y obtener tokens JWT",
    description="""
Valida las credenciales del usuario y retorna tokens JWT si son correctas.
- Requiere email y contraseña
- Solo usuarios activos pueden iniciar sesión
- Retorna access_token y refresh_token
""",
    response_model=UsuarioLoginResponse,
    responses={
        200: {"description": "Login exitoso con tokens JWT"},
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
                u_rol=usuario['u_rol'],
                access_token=usuario['access_token'],
                refresh_token=usuario['refresh_token'],
                token_type="bearer",
                mensaje="Login exitoso"
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Email o contraseña incorrectos"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor: " + str(e)
        ) from e


@router.post(
    "/usuarios/refresh",
    summary="Renovar access token",
    description="Genera un nuevo access token usando el refresh token",
    response_model=TokenResponse,
    responses={
        200: {"description": "Token renovado exitosamente"},
        401: {"description": "Refresh token inválido"}
    }
)
def refresh_token(token_data: TokenRefresh,
                  usuario_service: UsuarioService = Depends(get_usuario_service)):
    try:
        access_token = usuario_service.refresh_access_token(
            token_data.refresh_token)
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor") from e


@router.delete(
    "/usuarios/{u_id}",
    summary="Eliminar usuario y persona",
    description="Elimina un usuario y la persona asociada por ID de usuario. Requiere rol productor-admin.",
    response_model=APIResponse,
    responses={
        200: {"description": "Usuario y persona eliminados exitosamente"},
        401: {"description": "No autenticado o token inválido"},
        403: {"description": "No tiene permisos (requiere rol productor-admin)"},
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Error al eliminar"}
    }
)
def eliminar_usuario(
    u_id: int,
    current_user: dict = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    # Verificar que el usuario tiene rol productor-admin
    if current_user.get('rol') != RolEnum.PRODUCTOR_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para eliminar usuarios. Se requiere rol productor-admin"
        )

    try:
        usuario_service.eliminar_usuario_y_persona(u_id)
        data = {"u_id": u_id}
        return APIResponse(
            status="success",
            message="Usuario y persona eliminados exitosamente",
            data=data
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Error al eliminar usuario"
        )

@router.get(
    "/usuarios/me",
    summary="Obtener usuario autenticado",
    description="Devuelve los datos del usuario actual según el email del token.",
    response_model=APIResponse,
    responses={
        200: {"description": "Usuario autenticado encontrado"},
        401: {"description": "No autenticado o token inválido"},
        404: {"description": "Usuario no encontrado"}
    }
)
def obtener_usuario_actual(
    current_user: dict = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    try:
        email = current_user.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido o sin email")

        usuario = usuario_service.usuario_repository.find_by_email(email)
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuario con email {email} no encontrado")

        persona = None
        if getattr(usuario, "p_id", None):
            persona = usuario_service.persona_repository.find_by_id(usuario.p_id)

        data = {
            "u_id": usuario.u_id,
            "nombres": persona.p_nombre if persona else None,
            "apellidos": persona.p_apellido if persona else None,
            "email": usuario.u_email,
            "rol": usuario.u_rol
        }

        return APIResponse(status="success", message="Usuario autenticado", data=data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e