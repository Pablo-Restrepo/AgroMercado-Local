from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from microservice_user.api.routes import api_router
from microservice_user.infrastructure.db import PersonaRepository, UsuarioRepository
from microservice_user.application.services import UsuarioService
from microservice_user.infrastructure.engine import init_db
from py_eureka_client.eureka_client import EurekaClient
from microservice_user.core.config import settings

eureka_client = EurekaClient(
    eureka_server=settings.EUREKA_SERVER_URL,
    app_name=settings.EUREKA_APP_NAME,
    instance_port=settings.EUREKA_INSTANCE_PORT,
    instance_host="localhost",
)
init_db()
#TODO: Configurar el inicio de la aplicación con Lifespan
async def lifespan(app: FastAPI):
    await eureka_client.start()
    try:
        yield
    finally:
        # parar eureka_client
        await eureka_client.stop()


app = FastAPI(
    title="Microservicio de Usuarios",
    description="API para gestión de usuarios y autenticación JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

usuario_repository = UsuarioRepository()
db = PersonaRepository()
usuario_service = UsuarioService(usuario_repository, db)

app.include_router(api_router)




@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "microservice_user",
        "version": "1.0.0"
    }
