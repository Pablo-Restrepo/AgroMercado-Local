
from core.events.rabbit_config import RabbitConsumer, RabbitPublisher
from .event_manager import EventManager
from ..config import settings
# Instancia global reutilizable
event_manager = EventManager()

rabbit_url = settings.RABBIT_URL
queue_registro_productores = settings.PRODUCTORES_QUEUE
queue_creacion_productos = settings.PRODUCTOS_CREADOS_QUEUE
queue_actualizacion_productos = settings.PRODUCTOS_ACTUALIZADOS_QUEUE
queue_actualizacion_stock_productos = settings.PRODUCTOS_STOCK_ACTUALIZADO_QUEUE
consumer = RabbitConsumer(rabbit_url, 
                        queue_registro_productores_nombre = queue_registro_productores,
                         queue_actualizacion_stock_nombre=queue_actualizacion_stock_productos, prefetch=5)
publisher = RabbitPublisher(rabbit_url, 
                        queue_productos_actualizados = queue_actualizacion_productos,
                        queue_productos_creados=queue_creacion_productos)
