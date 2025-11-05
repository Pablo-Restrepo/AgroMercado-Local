from fastapi import Depends

from application.producto_service import ProductoService
from infrastructure.mongo_repository import MongoQueryRepository
from infrastructure.sql_repository import SQLCommandRepository

def get_producto_query_repository():
    """
    Retorna una instancia del repositorio de consultas basado en MongoDB.
    """
    return MongoQueryRepository()


def get_producto_command_repository():
    """
    Retorna una instancia del repositorio de comandos basado en SQL.
    """
    return SQLCommandRepository()


def get_producto_service():
    query_repo = MongoQueryRepository()
    command_repo = SQLCommandRepository()
    return ProductoService(
        query_repo=query_repo,
        command_repo=command_repo
    )

