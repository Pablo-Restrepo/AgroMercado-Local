from typing import Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class ClientNotFound(Exception):
    pass


def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_exceptions(app: FastAPI):
    app.add_exception_handler(
        ClientNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={'message': 'Client not found',
                            'error_code': 'client_not_found'},
        ),
    )

    """ @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        return JSONResponse(
            content={
                'message': 'Oops! Something went wrong',
                'error_code': 'server_error',
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) """
