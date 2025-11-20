from fastapi import FastAPI, logger
from fastapi.responses import RedirectResponse
from api import producto_controller
from api.producto_controller import ProductoController

from fastapi import FastAPI
from contextlib import asynccontextmanager

from application.consumer_handlers import handle_create_productor
from core.dependencies import get_producto_service
from core.events import event_manager
from core.events.handler import on_producto_creado
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
    # crear instancia del servicio para inyectar en el handler
    producto_service = get_producto_service()

    # configurar consumer
    rabbit_url = settings.RABBIT_URL
    queue = settings.PRODUCTORS_QUEUE
    consumer = RabbitConsumer(rabbit_url, queue, prefetch=5)
    await consumer.connect()

    # wrapper handler para inyectar servicio
    async def _handler(payload: dict, message):
        await handle_create_productor(payload, message, producto_service)

    await consumer.start(_handler)
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