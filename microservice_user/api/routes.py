from fastapi import APIRouter
from microservice_user.api.controllers import router as usuario_router

api_router = APIRouter()
api_router.include_router(usuario_router, prefix="", tags=["usuarios"])