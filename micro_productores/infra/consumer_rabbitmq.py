import asyncio
import json
import logging
from typing import Callable, Awaitable, Optional

import aio_pika
from aio_pika import IncomingMessage

logger = logging.getLogger(__name__)

HandlerType = Callable[[dict, IncomingMessage], Awaitable[None]]

class RabbitConsumer:
    def __init__(self, amqp_url: str, queue_name: str, prefetch: int = 10):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.prefetch = prefetch
        self._conn: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.RobustChannel] = None
        self._queue: Optional[aio_pika.Queue] = None
        self._task: Optional[asyncio.Task] = None
        self._handler: Optional[HandlerType] = None

    async def connect(self):
        self._conn = await aio_pika.connect_robust(self.amqp_url)
        self._channel = await self._conn.channel()
        await self._channel.set_qos(prefetch_count=self.prefetch)
        self._queue = await self._channel.declare_queue(self.queue_name, durable=True)
        logger.info("RabbitConsumer connected queue=%s", self.queue_name)

    async def start(self, handler: HandlerType):
        if not self._queue:
            raise RuntimeError("connect() must be called before start()")
        self._handler = handler
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self):
        try:
            async with self._queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await self._on_message(message)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        # Log inside _on_message and nack accordingly
                        logger.exception("Unhandled error processing message")
        except asyncio.CancelledError:
            logger.info("Consumer loop cancelled")
            raise
        except Exception:
            logger.exception("Consumer loop error, will exit task")

    async def _on_message(self, message: IncomingMessage):
        async with message.process(requeue=False):
            if not self._handler:
                logger.warning("No handler configured, rejecting message")
                return
            try:
                body = message.body.decode() if message.body else "{}"
                payload = json.loads(body)
            except Exception:
                logger.exception("Invalid JSON in message body")
                # al salir del context manager, message procesado -> ack/nack según exceptions
                return

            await self._handler(payload, message)

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._channel:
            await self._channel.close()
        if self._conn:
            await self._conn.close()
        logger.info("RabbitConsumer stopped")