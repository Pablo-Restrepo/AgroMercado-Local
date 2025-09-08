from fastapi import APIRouter
from app.api.v1.endpoints import cliente, pedidoController, productoController

api_router = APIRouter()

api_router.include_router(cliente.router)
api_router.include_router(pedidoController.router)
api_router.include_router(productoController.router)

