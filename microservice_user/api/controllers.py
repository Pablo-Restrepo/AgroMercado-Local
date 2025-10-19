from fastapi import APIRouter, HTTPException, Depends
from microservice_user.api.schemas import UsuarioRegistro
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