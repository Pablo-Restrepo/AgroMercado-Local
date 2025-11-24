from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.v1.gremio_controller import router as gremio_controller 
from api.v1.productor_controller import router as productor_controller 
from config import settings
from infra.logging import logger
from fastapi import FastAPI
from contextlib import asynccontextmanager

from infra.db.engine import init_db, close_db
from deps import get_productor_service, eureka_client
from application.handler import handle_create_productor_admin
from infra.consumer_rabbitmq import RabbitConsumer

@asynccontextmanager
async def lifespan(app: FastAPI):
     # iniciar DB
    await init_db()

    # crear instancia del servicio para inyectar en el handler
    productor_service = get_productor_service()    

    # configurar consumer
    rabbit_url = settings.RABBIT_URL
    queue = settings.QUEUE_NAME
    consumer = RabbitConsumer(rabbit_url, queue, prefetch=5)
    await consumer.connect()

    # wrapper handler para inyectar servicio
    async def _handler(payload: dict, message):
        await handle_create_productor_admin(payload, message, productor_service)

    await consumer.start(_handler)
    app.state.rabbit_consumer = consumer
    #registrar en Eureka
    try:
        await eureka_client.start() 
        #pass # Se desactiva el registro mientras se configura la autorización
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
        await close_db()


app = FastAPI(title="Microservicio de Productores", version="1.0.0",lifespan=lifespan)
app.include_router(productor_controller)
app.include_router(gremio_controller)


@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')