from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.v1.gremio_controller import router as gremio_controller 
from api.v1.productor_controller import router as productor_controller 
#from infra.messaging import RabbitPublisher
from config import settings

from fastapi import FastAPI
from contextlib import asynccontextmanager

from infra.db.engine import init_db
from deps import get_publisher

async def handle_message(payload: dict):
    # Lógica para manejar el mensaje recibido
    print("Mensaje recibido:", payload)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicio
    """pub = get_publisher()
    await pub.connect()
    await pub.start_consuming(handle_message)
    app.state.rabbit_publisher = pub"""
    await init_db()
    try:
        # yield permite que FastAPI sirva peticiones mientras el contexto está activo
        yield
    finally:
        if hasattr(app.state, "rabbit_publisher"):
            await app.state.rabbit_publisher.stop()

#Incluir "lifespan=lifespan" cuando se implemente RabbitMQ
app = FastAPI(title="Microservicio de Productores", version="1.0.0",lifespan=lifespan)
app.include_router(productor_controller)
app.include_router(gremio_controller)


@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')