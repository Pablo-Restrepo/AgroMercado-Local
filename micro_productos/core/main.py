from fastapi import FastAPI, logger
from fastapi.responses import RedirectResponse
from api import producto_controller
from api.producto_controller import ProductoController

from fastapi import FastAPI
from contextlib import asynccontextmanager

from application.consumer_handlers import handle_create_productor_admin, handle_create_productor_asociados
from core.dependencies import get_producto_service
from core.events import event_manager
from core.events.handler import on_producto_actualizado, on_producto_creado, on_producto_eliminado
from infrastructure.db.mongo_engine import init_mongo_db, close_mongo_db
from infrastructure.db.sql_engine import close_sql_db, init_sql_db
from infrastructure.db import sql_engine
from .eureka_registry import eureka_client
from .events.rabbit_config import RabbitConsumer
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
     # iniciar DB SQL
    await init_sql_db()
     # iniciar DB MONGO
    init_mongo_db()

    "iniciar el manejerador de eventos"
    event_manager.subscribe("producto_creado", on_producto_creado)
    event_manager.subscribe("producto_eliminado",on_producto_eliminado)
    event_manager.subscribe("producto_actualizado",on_producto_actualizado)
    # crear instancia del servicio para inyectar en el handler
    producto_service = get_producto_service()

    # configurar consumer
    rabbit_url = settings.RABBIT_URL
    queue_registro_productores_asociados = settings.PRODUCTORES_ASOCIADOS_QUEUE
    queue_registro_productores_admin = settings.PRODUCTORES_ADMIN_QUEUE
    consumer = RabbitConsumer(rabbit_url, 
                            queue_registro_productores_asociados_nombre = queue_registro_productores_asociados,
                            queue_registro_productores_admin_nombre=queue_registro_productores_admin, prefetch=5)
    await consumer.connect()

    # wrapper handler para inyectar servicio
    async def _handler_productor_asociados(payload: dict, message):
        await handle_create_productor_asociados(payload, message, producto_service)

    async def _handler_productor_admin(payload: dict, message):
        await handle_create_productor_admin(payload, message, producto_service)

    await consumer.start_asociados(_handler_productor_asociados)
    app.state.rabbit_consumer = consumer
    #registrar en Eureka
    try:
        await eureka_client.start() 
    except Exception as e:        
        logger.error(f"Error al registrar en Eureka: {e}")
        pass

    try:
        yield
    finally:
        # parar consumer
        await consumer.stop()
        # parar eureka_client
        await eureka_client.stop()
        # cerrar conexión DB
        await close_sql_db()
        close_mongo_db()


producto_service = get_producto_service()
producto_controller = ProductoController(producto_service)
app = FastAPI(title="Microservicio de Productos", version="1.0.0",lifespan=lifespan)
app.include_router(producto_controller.router)


@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')