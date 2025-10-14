from fastapi import APIRouter, HTTPException, Depends
from microservice_user.api.schemas import UsuarioRegistro
from microservice_user.domain.usuario import Usuario
from microservice_user.application.services import UsuarioService

router = APIRouter()

def get_usuario_service():
    # Importa aquí para evitar problemas de import circular
    from microservice_user.api.main import usuario_service
    return usuario_service

@router.post("/usuarios/registro")
def registrar_usuario(
    usuario_data: UsuarioRegistro,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    try:
        usuario = Usuario(
            u_id=None,
            u_nombre_usuario=usuario_data.u_nombre_usuario,
            u_contrasenia=usuario_data.u_contrasenia,
            u_email=usuario_data.u_email,
            p_id=usuario_data.p_id
        )
        usuario_service.registrar_usuario(usuario)
        return {"mensaje": "Usuario registrado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))