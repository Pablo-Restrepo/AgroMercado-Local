import json
from typing import List
import pika
from core.config import settings
from infraestructure.logging import logger
from domain.entities.producto_unitario import ProductoUnitario

RABBITMQ_URL = settings.RABBIT_URL
UPDATE_STOCK_QUEUE_NAME = settings.PRODUCT_STOCK_QUEUE_NAME

def _get_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)

def publish_stock_updates(productos_unitarios: List[ProductoUnitario], queue: str = UPDATE_STOCK_QUEUE_NAME) -> None:
    """
    Publica un JSON con la información necesaria para actualizar el stock en el microservicio de productos
    """
    #Convertir todos los productos unitarios a una lista de productos tipo {"p_id"=...,"cant"=...}    
    payload = []
    for pu in productos_unitarios:
        payload.append(
            {"p_id": pu.id_producto, "cant": pu.cantidad}
            )
    conn = _get_connection()
    try:
        ch = conn.channel()
        ch.queue_declare(queue=queue, durable=True)
        body = json.dumps(payload)
        ch.basic_publish(
            exchange="",
            routing_key=queue,
            body=body,
            properties=pika.BasicProperties(content_type="application/json", delivery_mode=2)
        )
        logger.info(f"Publicado en cola {queue}: {body}")
    finally:
        conn.close()
#TODO
def publish_stock_updates(productos_unitarios: List[ProductoUnitario], queue: str = UPDATE_STOCK_QUEUE_NAME) -> None:
    """
    Publica un JSON con la información necesaria para mandar el envío de una compra al microservicio de productores
    """
    #Convertir todos los productos unitarios a una lista de productos tipo {"p_id"=...,"cant"=...}    
    payload = []
    for pu in productos_unitarios:
        payload.append(
            {"p_id": pu.id_producto, "cant": pu.cantidad}
            )
    conn = _get_connection()
    try:
        ch = conn.channel()
        ch.queue_declare(queue=queue, durable=True)
        body = json.dumps(payload)
        ch.basic_publish(
            exchange="",
            routing_key=queue,
            body=body,
            properties=pika.BasicProperties(content_type="application/json", delivery_mode=2)
        )
        logger.info(f"Publicado en cola {queue}: {body}")
    finally:
        conn.close()