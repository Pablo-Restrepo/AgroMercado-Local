import json
import pika
from core.config import settings
from infraestructure.logging import logger

RABBITMQ_URL = settings.RABBIT_URL
QUEUE_NAME = settings.PRODUCTORS_QUEUE

def _get_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)

#TODO Cambiar publicador
def publish_productor_registration(payload: dict, queue: str = None) -> None:
    """
    Publica JSON en la cola RabbitMQ (durable). Payload debe contener
    solo los atributos que quieres enviar: 
    """
    q = queue or QUEUE_NAME
    conn = _get_connection()
    try:
        ch = conn.channel()
        ch.queue_declare(queue=q, durable=True)
        body = json.dumps(payload)
        ch.basic_publish(
            exchange="",
            routing_key=q,
            body=body,
            properties=pika.BasicProperties(content_type="application/json", delivery_mode=2)
        )
        logger.info(f"Publicado en cola {q}: {body}")
    finally:
        conn.close()