from fastapi import FastAPI
from microservice_user.api.routes import api_router
from microservice_user.infrastructure.db import PersonaRepository, UsuarioRepository, init_db
from microservice_user.application.services import UsuarioService

# Inicializar la base de datos
init_db()

app = FastAPI()

usuario_repository = UsuarioRepository()
persona_repository = PersonaRepository()
usuario_service = UsuarioService(usuario_repository, persona_repository)

app.include_router(api_router)
