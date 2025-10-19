from fastapi import FastAPI
from microservice_user.api.routes import api_router
from microservice_user.infrastructure.db import PersonaRepository, UsuarioRepository
from microservice_user.infrastructure.db_config import db_config
from microservice_user.application.services import UsuarioService
from microservice_user.infrastructure.engine import init_db

app = FastAPI(title="Microservicio de Usuarios", version="1.0.0")

# Inicializar la base de datos
init_db()

# Inyección de dependencias
usuario_repository = UsuarioRepository(db_config)
persona_repository = PersonaRepository(db_config)
usuario_service = UsuarioService(usuario_repository, persona_repository)

app.include_router(api_router)