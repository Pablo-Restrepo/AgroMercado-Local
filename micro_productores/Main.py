from fastapi import FastAPI
from api.v1.productor_router import productor_router
from api.v1.gremio_router import gremio_router
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
app.include_router(productor_router, prefix="/api/v1/productores", tags=["Productores"])
app.include_router(gremio_router, prefix="/api/v1/gremios", tags=["Gremios"])
