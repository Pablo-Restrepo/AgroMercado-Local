from application.services import ProductoService, UsuarioService
from infraestructure.logging import logger
from aio_pika import IncomingMessage
from application.dtos import ProductoDTO, UsuarioDTO
from deps import get_producto_service, get_usuario_service

#Manejador para recibir un usuario creado desde otro microservicio
async def handle_create_usuario(payload, message: IncomingMessage, usuario_service: UsuarioService=get_usuario_service()):
    # Validar entrada con Pydantic
    try:
        #data = json.loads(payload)
        dto = UsuarioDTO.model_validate(payload)
    except Exception as e:
        logger.warning("Invalid message payload, rejecting: %s", e)
        # no requeue (message.process requeue=False) -> se ack/nack al salir con excepción
        raise    
    try:        
        created = await usuario_service.crear_usuario(dto)
        # Si todo OK, simplemente return (message context manager hará ack)
        logger.info("Usuario creado desde mensaje OK: %s", created)
    except Exception as e:
        logger.exception("Error creando usuario desde mensaje: %s", e)
        # lanzar excepción para que el message.process haga nack (requeue=False) o manejar retento/DLQ aquí
        raise
#Manejador para recibir un prodcuto creado desde otro microservicio
async def handle_create_producto(payload, message: IncomingMessage, producto_service: ProductoService=get_producto_service()):
    # Validar entrada con Pydantic
    try:
        #data = json.loads(payload)
        dto = ProductoDTO.model_validate(payload)
    except Exception as e:
        logger.warning("Invalid message payload, rejecting: %s", e)
        # no requeue (message.process requeue=False) -> se ack/nack al salir con excepción
        raise    
    try:        
        created = await producto_service.crear_producto(dto)
        # Si todo OK, simplemente return (message context manager hará ack)
        logger.info("Producto creado desde mensaje OK: %s", created)
    except Exception as e:
        logger.exception("Error creando producto desde mensaje: %s", e)
        # lanzar excepción para que el message.process haga nack (requeue=False) o manejar retento/DLQ aquí
        raise