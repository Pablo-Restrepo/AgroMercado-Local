from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.producto_controller import ProductoController

from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.dependencies import get_producto_service
from core.events import event_manager
from core.events.handler import on_producto_creado
from infrastructure.db.mongo_engine import init_mongo_db, close_mongo_db
from infrastructure.db.sql_engine import init_sql_db
from infrastructure.db import sql_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
     # iniciar DB
    await init_sql_db()
    init_mongo_db()

     # Registrar observadores
    event_manager.subscribe("producto_creado", on_producto_creado)
    try:
        yield
    finally:
        close_mongo_db()
        # parar consumer
        





producto_service = get_producto_service()
producto_controller = ProductoController(producto_service)

app = FastAPI(title="Microservicio de Productos", version="1.0.0",lifespan=lifespan)
app.include_router(producto_controller.router)


@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')