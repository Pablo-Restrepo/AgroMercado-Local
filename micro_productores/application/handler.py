import json
from micro_compras.infraestructure.logging import logger
from aio_pika import IncomingMessage
from application.dtos import CrearProductorDTO
from application.services import ProductorService

async def handle_create_productor_admin(payload, message: IncomingMessage, productor_service: ProductorService):
    # Validar entrada con Pydantic
    try:
        #data = json.loads(payload)
        dto = CrearProductorDTO.model_validate(payload)
    except Exception as e:
        logger.warning("Invalid message payload, rejecting: %s", e)
        # no requeue (message.process requeue=False) -> se ack/nack al salir con excepción
        raise    
    try:        
        created = await productor_service.crear_admin(dto)
        # Si todo OK, simplemente return (message context manager hará ack)
        logger.info("Productor creado desde mensaje OK: %s", created)
    except Exception as e:
        logger.exception("Error creando productor desde mensaje: %s", e)
        # lanzar excepción para que el message.process haga nack (requeue=False) o manejar retento/DLQ aquí
        raise