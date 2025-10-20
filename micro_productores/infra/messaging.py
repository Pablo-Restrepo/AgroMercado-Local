import asyncio
import json
import logging
from typing import Callable, Awaitable, Any, Optional

import aio_pika

logger = logging.getLogger(__name__)

HandlerType = Callable[[dict], Awaitable[None]]

class RabbitConsumer:
    def __init__(self, amqp_url: str, queue_name: str, prefetch: int = 10):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.prefetch = prefetch
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None
        self._consumer_tag = None
        self._task: Optional[asyncio.Task] = None
        self._handler: Optional[HandlerType] = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.prefetch)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        logger.info("RabbitMQ connected, queue=%s", self.queue_name)

    async def start(self, handler: HandlerType) -> None:
        if not self.queue:
            raise RuntimeError("connect() must be called before start()")
        self._handler = handler
        # start consuming in background so it doesn't block startup
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self) -> None:
        try:
            self._consumer_tag = await self.queue.consume(self._on_message)
            # keep task alive until cancelled
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled")
            raise
        except Exception:
            logger.exception("Error in consume loop")

    async def _on_message(self, message: aio_pika.IncomingMessage) -> None:
        async with message.process(requeue=False):
            try:
                body = message.body.decode()
                payload = json.loads(body) if body else {}
                if self._handler:
                    await self._handler(payload)
            except Exception:
                logger.exception("Failed to process message")
                # raising inside process context will nack the message (requeue=False)

    async def stop(self) -> None:
        # cancel background task
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self.queue and self._consumer_tag:
            try:
                await self.queue.cancel(self._consumer_tag)
            except Exception:
                logger.exception("Error cancelling consumer")
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.info("RabbitMQ disconnected")
