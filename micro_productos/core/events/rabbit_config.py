import asyncio
import json
import logging
from typing import Callable, Awaitable, Optional

import aio_pika
from aio_pika import IncomingMessage

logger = logging.getLogger(__name__)

HandlerType = Callable[[dict, IncomingMessage], Awaitable[None]]

class RabbitConsumer:
    def __init__(self, amqp_url: str, queue_registro_productores_asociados_nombre: str, queue_registro_productores_admin_nombre:str, prefetch: int = 10):
        self.amqp_url = amqp_url
        self.queue_registro_productores_asociados_nombre = queue_registro_productores_asociados_nombre
        self.queue_registro_productores_admin_nombre = queue_registro_productores_admin_nombre
        self.prefetch = prefetch
        self._conn: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.RobustChannel] = None
        self._queue_registro_productores_asociados: Optional[aio_pika.Queue] = None
        self._queue_registro_productores_admin: Optional[aio_pika.Queue] = None
        self._task: Optional[asyncio.Task] = None
        self._handler: Optional[HandlerType] = None

    async def connect(self):
        self._conn = await aio_pika.connect_robust(self.amqp_url)
        self._channel = await self._conn.channel()

        await self._channel.set_qos(prefetch_count=self.prefetch)

        # Declarar colas
        self._queue_registro_productores_asociados = await self._channel.declare_queue(
            self.queue_registro_productores_asociados_nombre, durable=True
        )
        self._queue_registro_productores_admin = await self._channel.declare_queue(
            self.queue_registro_productores_admin_nombre, durable=True
        )

        logger.info("RabbitConsumer connected: asociados=%s admin=%s",
                    self.queue_registro_productores_asociados_nombre,
                    self.queue_registro_productores_admin_nombre)

     # ---------------------------
    # CONSUMO: COLA ASOCIADOS
    # ---------------------------
    async def start_asociados(self, handler_asociados: HandlerType):
        if not self._queue_registro_productores_asociados:
            raise RuntimeError("connect() must be called before start()")

        self._handler_asociados = handler_asociados
        self._task_asociados = asyncio.create_task(self._consume_loop_asociados())

    async def _consume_loop_asociados(self):
        try:
            async with self._queue_registro_productores_asociados.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await self._on_message(message, self._handler_asociados)
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
    # CONSUMO: COLA ADMIN
    # ---------------------------
    async def start_admin(self, handler_admin: HandlerType):
        if not self._queue_registro_productores_admin:
            raise RuntimeError("connect() must be called before start_admin()")

        self._handler_admin = handler_admin
        self._task_admin = asyncio.create_task(self._consume_loop_admin())

    async def _consume_loop_admin(self):
        try:
            async with self._queue_registro_productores_admin.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await self._on_message(message, self._handler_admin)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        logger.exception("Unhandled error processing message (admin)")
        except asyncio.CancelledError:
            logger.info("Consumer admin cancelled")
            raise
        except Exception:
            logger.exception("Consumer admin error")

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
        for task in [self._task_asociados, self._task_admin]:
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