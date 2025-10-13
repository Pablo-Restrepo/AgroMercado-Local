from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.v1.gremio_controller import router as gremio_controller 
from api.v1.productor_controller import router as productor_controller 
#from infra.messaging import RabbitPublisher
from config import settings

from fastapi import FastAPI
from contextlib import asynccontextmanager

"""
async def lifespan(app: FastAPI):
    # Código de inicio
    pub = RabbitPublisher(settings.RABBIT_URL)
    await pub.connect()
    app.state.publisher = pub
    yield
    # Código de cierre
    if hasattr(app.state, "publisher"):
        await app.state.publisher._conn.close()
"""
#Incluir "lifespan=lifespan" cuando se implemente RabbitMQ
app = FastAPI(title="Microservicio de Productores", version="1.0.0")
app.include_router(productor_controller)
app.include_router(gremio_controller)
@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')