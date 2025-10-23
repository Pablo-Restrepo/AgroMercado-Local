import os
import json
import pika
import time

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME = os.getenv("USER_REG_QUEUE", "user_registrations")

def _get_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)

def handle_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        u_id = data.get("u_id")
        nombres = data.get("nombres")
        apellidos = data.get("apellidos")
        # Procesamiento: enviar email, log, notificar otro servicio, etc.
        print("Procesando registro de usuario:", u_id, nombres, apellidos)
        # ack
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as ex:
        print("Error procesando mensaje:", ex)
        # opcional: nack con requeue=False para evitar loops
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    while True:
        try:
            conn = _get_connection()
            ch = conn.channel()
            ch.queue_declare(queue=QUEUE_NAME, durable=True)
            ch.basic_qos(prefetch_count=1)
            ch.basic_consume(queue=QUEUE_NAME, on_message_callback=handle_message)
            print(f"Subscribed to {QUEUE_NAME}, waiting messages...")
            ch.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print("RabbitMQ connection error, retrying in 5s...", e)
            time.sleep(5)

if __name__ == "__main__":
    main()