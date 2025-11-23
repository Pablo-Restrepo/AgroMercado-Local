import asyncio
import json
import logging
from typing import Callable, Awaitable, Optional

import aio_pika
from aio_pika import IncomingMessage

logger = logging.getLogger(__name__)

HandlerType = Callable[[dict, IncomingMessage], Awaitable[None]]

class RabbitConsumer:
    def __init__(self, amqp_url: str, queue_registro_productores_nombre: str, queue_actualizacion_stock_nombre:str, prefetch: int = 10):
        self.amqp_url = amqp_url
        self.queue_registro_productores_nombre = queue_registro_productores_nombre
        self.queue_actualizacion_stock_nombre = queue_actualizacion_stock_nombre
        self.prefetch = prefetch
        self._conn: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.RobustChannel] = None
        self._queue_registro_productores: Optional[aio_pika.Queue] = None
        self._queue_actualizacion_stock: Optional[aio_pika.Queue] = None
        self._task: Optional[asyncio.Task] = None
        self._handler: Optional[HandlerType] = None

    async def connect(self):
        self._conn = await aio_pika.connect_robust(self.amqp_url)
        self._channel = await self._conn.channel()

        await self._channel.set_qos(prefetch_count=self.prefetch)

        # Declarar colas
        self._queue_registro_productores = await self._channel.declare_queue(
            self.queue_registro_productores_nombre, durable=True
        )

        self._queue_actualizacion_stock = await self._channel.declare_queue(
            self.queue_actualizacion_stock_nombre, durable=True
        )

        logger.info("RabbitConsumer connected: productores=%s, actualizacion stock=%s",
                    self.queue_registro_productores_nombre, self.queue_actualizacion_stock_nombre)

     # ---------------------------
    # CONSUMO: COLA PRODUCTORES
    # ---------------------------
    async def start_productores(self, handler_productores: HandlerType):
        if not self._queue_registro_productores:
            raise RuntimeError("connect() must be called before start()")

        self._handler_productores = handler_productores
        self._task_productores = asyncio.create_task(self._consume_loop_productores())

    async def _consume_loop_productores(self):
        try:
            async with self._queue_registro_productores.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await self._on_message(message, self._handler_productores)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        logger.exception("Unhandled error processing message (asociados)")
        except asyncio.CancelledError:
            logger.info("Consumer asociados cancelled")
            raise
        except Exception:
            logger.exception("Consumer asociados error")


     # ---------------------------
    # CONSUMO: COLA ACTUALIZACION STOCK
    # ---------------------------
    async def start_actualizacion_stock(self, handler_actualizacion_stock: HandlerType):
        if not self._queue_actualizacion_stock:
            raise RuntimeError("connect() must be called before start()")

        self._handler_actualizacion_stock= handler_actualizacion_stock
        self._task_actualizacion_stock = asyncio.create_task(self._consume_loop_actualizacion_stock())

    async def _consume_loop_actualizacion_stock(self):
        try:
            async with self._queue_actualizacion_stock.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await self._on_message(message, self._handler_actualizacion_stock)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        logger.exception("Unhandled error processing message (asociados)")
        except asyncio.CancelledError:
            logger.info("Consumer asociados cancelled")
            raise
        except Exception:
            logger.exception("Consumer asociados error")


    # ---------------------------
    # MANEJO DE MENSAJE
    # ---------------------------
    async def _on_message(self, message: IncomingMessage, handler: HandlerType):
        async with message.process(requeue=False):
            if not handler:
                logger.warning("No handler configured, rejecting message")
                return
            try:
                body = message.body.decode() if message.body else "{}"
                payload = json.loads(body)
            except Exception:
                logger.exception("Invalid JSON in message body")
                return

            await handler(payload, message)

    # ---------------------------
    # STOP
    # ---------------------------
    async def stop(self):
        for task in [self._task_productores, self._task_admin]:
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        if self._channel:
            await self._channel.close()
        if self._conn:
            await self._conn.close()

        logger.info("RabbitConsumer stopped")


class RabbitPublisher:
    def __init__(self, amqp_url: str, queue_productos_actualizados:str, queue_productos_creados:str):
        self.amqp_url = amqp_url
        self.queue_productos_actualizados_nombre = queue_productos_actualizados
        self.queue_productos_creados_nombre = queue_productos_creados
        self._conn: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.RobustChannel] = None
        self._queue_productos_creados: Optional[aio_pika.Queue] = None
        self._queue_productos_actualizados: Optional[aio_pika.Queue] = None

    async def connect(self):
        """Conecta al broker RabbitMQ y abre un canal."""
        self._conn = await aio_pika.connect_robust(self.amqp_url)
        self._channel = await self._conn.channel(publisher_confirms=True)

        # Declarar colas
        self._queue_productos_creados = await self._channel.declare_queue(
            self.queue_productos_creados_nombre, durable=True
        )
        self._queue_productos_actualizados = await self._channel.declare_queue(
            self.queue_productos_actualizados_nombre, durable=True
        )
        logger.info("RabbitPublisher connected, colas: %s %s",self.queue_productos_creados_nombre,
                                                            self.queue_productos_actualizados_nombre)

    async def publish(
        self,
        message: dict,
        *,
        routing_key: str,
        exchange_name: str = "",
        persistent: bool = True
    ):
        """
        Publica un mensaje JSON en RabbitMQ.

        - exchange_name = ""  →  default exchange (direct to queue)
        - routing_key = nombre de la cola o routing key
        """

        if not self._channel:
            raise RuntimeError("connect() must be called before publish()")

        try:
            body = json.dumps(message).encode()
        except Exception as e:
            logger.error("Error converting message to JSON: %s", e)
            raise


        msg = aio_pika.Message(
            body=body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT if persistent else aio_pika.DeliveryMode.NOT_PERSISTENT
        )
        try:
            await self._channel.default_exchange.publish(msg, routing_key=routing_key)
            
            logger.info("Message published to %s -> %s", exchange_name or "[default]", routing_key)
        except Exception:
            logger.exception("Failed to publish message")
            raise

    async def close(self):
        """Cierra el canal y la conexión."""
        if self._channel:
            await self._channel.close()
        if self._conn:
            await self._conn.close()

        logger.info("RabbitPublisher closed")