from fastapi import FastAPI
from microservice_user.api.routes import api_router
from microservice_user.infrastructure.db import PersonaRepository, UsuarioRepository
from microservice_user.infrastructure.db_config import db_config
from microservice_user.application.services import UsuarioService

app = FastAPI()


usuario_repository = UsuarioRepository(db_config)
persona_repository = PersonaRepository(db_config)
usuario_service = UsuarioService(usuario_repository, persona_repository)

app.include_router(api_router)