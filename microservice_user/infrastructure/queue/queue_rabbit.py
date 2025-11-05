import os
import json
import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME = os.getenv("USER_REG_QUEUE", "user_registrations")

def _get_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)

def publish_user_registration(payload: dict, queue: str = None) -> None:
    """
    Publica JSON en la cola RabbitMQ (durable). Payload debe contener
    solo los atributos que quieres enviar: {"u_id", "nombres", "apellidos"}.
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
    finally:
        conn.close()