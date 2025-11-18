from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.exceptions import register_exception_handlers
from api.compra_controller import router as compra_router
from infraestructure.db.engine import close_db, init_db

async def lifespan(app: FastAPI):
    await init_db()
    # Aquí puedes agregar lógica de inicio y cierre si es necesario
    try:
        yield
    finally:
        # parar consumer
        #await consumer.stop()
        # parar eureka_client
        #await eureka_client.stop()
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

@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')