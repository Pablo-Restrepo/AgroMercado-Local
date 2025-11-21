import json
from infrastructure.logging import logger
from aio_pika import IncomingMessage
from api.esquemas import ProductorRegistroConsulta
from application.producto_service import ProductoService



async def handle_create_productor(payload, message: IncomingMessage, productor_service: ProductoService):
    # Validar entrada con Pydantic
    try:
        #data = json.loads(payload)
        dto = ProductorRegistroConsulta.model_validate(payload)
    except Exception as e:
        logger.warning("Invalid message payload, rejecting: %s", e)
        # no requeue (message.process requeue=False) -> se ack/nack al salir con excepción
        raise    
    try:        
        created = await productor_service.registrar_productor(dto)
        # Si todo OK, simplemente return (message context manager hará ack)
        logger.info("Productor creado desde mensaje OK: %s", created)
    except Exception as e:
        logger.exception("Error creando productor desde mensaje: %s", e)
        # lanzar excepción para que el message.process haga nack (requeue=False) o manejar retento/DLQ aquí
        raise

