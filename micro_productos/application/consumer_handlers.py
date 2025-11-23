import json

from pydantic import TypeAdapter
from infrastructure.logging import logger
from aio_pika import IncomingMessage
from api.esquemas import ProductoCompra, ProductorRegistroConsulta
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



async def handle_created_compra(payload, message: IncomingMessage, productor_service: ProductoService):
    """
        metodo que se encarga de recibir la informacion de las compras realizadas
        para actualizar el stock de los productos 
    """
    # Validar entrada con Pydantic
    try:
        datos_compra = TypeAdapter(list[ProductoCompra]).validate_python(payload)
    except Exception as e:
        logger.warning("Invalid message payload, rejecting: %s", e)
        # no requeue (message.process requeue=False) -> se ack/nack al salir con excepción
        raise ValueError("Invalid message payload")
    try:        
        actualizados = await productor_service.actualizar_stock_productos(datos_compra)
        # Si todo OK, simplemente return (message context manager hará ack)
        logger.info("# %s productos fueron actualizado correctamente", actualizados)
    except Exception as e:
        logger.exception("Error actualizando el stock de  productos desde mensaje: %s", e)
        # lanzar excepción para que el message.process haga nack (requeue=False) o manejar retento/DLQ aquí
        raise
