from fastapi import APIRouter
from app.api.v1.endpoints import (
    cliente
)

api_router = APIRouter()

api_router.include_router(cliente.router)
