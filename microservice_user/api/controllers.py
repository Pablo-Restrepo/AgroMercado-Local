from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from microservice_user.api.schemas import UsuarioRegistro
from microservice_user.application.mapper import usuario_registro_to_persona, usuario_registro_to_usuario
from microservice_user.application.services import UsuarioService
from microservice_user.api.response import APIResponse
from microservice_user.infrastructure.queue.queue_rabbit import publish_user_registration

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
            "apellidos": persona.p_apellido
        }

        # Encolar publicación en background para no bloquear la respuesta
        background_tasks.add_task(publish_user_registration, data)

        return APIResponse(status="success", message="Usuario y persona registrados exitosamente", data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))