from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.exceptions import register_exception_handlers
from api.compra_controller import router as compra_router
from api.envio_controller import router as envio_router
from infraestructure.broker.consumer_rabbitmq import RabbitConsumer
from infraestructure.db.engine import close_db, init_db
from core.config import settings
from deps import eureka_client
from application.handler import handle_create_producto, handle_create_usuario

async def lifespan(app: FastAPI):
    await init_db()    
    rabbit_url = settings.RABBIT_URL
    # configurar consumer para mensajes desde el micro de usuarios
    usuario_queue = settings.USUARIO_QUEUE_NAME
    usuario_consumer = RabbitConsumer(rabbit_url, usuario_queue, prefetch=5)
    await usuario_consumer.connect()

    # wrapper handler para inyectar servicio
    async def _handler_usuario_message(payload: dict, message):
        await handle_create_usuario(payload, message)

    await usuario_consumer.start(_handler_usuario_message)
    # configurar consumer para mensajes desde el micro de productos
    producto_queue = settings.PRODUCTO_QUEUE_NAME
    producto_consumer = RabbitConsumer(rabbit_url, producto_queue, prefetch=5)
    await producto_consumer.connect()

    # wrapper handler para inyectar servicio
    async def _handler_producto_message(payload: dict, message):
        await handle_create_producto(payload, message)

    await producto_consumer.start(_handler_producto_message)
    try:
        await eureka_client.start() 

    finally:
        # parar consumer
        await usuario_consumer.stop()
        await producto_consumer.stop()
        # parar eureka_client
        await eureka_client.stop()
        # cerrar conexión DB
        await close_db()
app = FastAPI(
    title="Microservicio de Compras",
    description="API para gestión de compras en AgroMercado Local",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)
register_exception_handlers(app)

app.include_router(compra_router)
app.include_router(envio_router)

@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004)