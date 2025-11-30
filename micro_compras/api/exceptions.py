from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions import DomainError

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        # respuesta consistente tipo problem-details / envoltorio "error"
        payload = {
            "error": {
                "code": getattr(exc, "code", "DOMAIN_ERROR"),
                "message": str(exc),
            }
        }
        return JSONResponse(status_code=getattr(exc, "status_code", 400), content=payload)

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # fallback genérico (no leak de detalles sensibles)
        payload = {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Error interno"
            }
        }
        return JSONResponse(status_code=500, content=payload)