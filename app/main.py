import threading
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db, seed_data, SessionLocal
from app.core.exceptions import register_all_exceptions
from app.core.middleware import register_middleware
from contextlib import asynccontextmanager

init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    seed_data(db)
    db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,lifespan=lifespan
)



register_all_exceptions(app)
register_middleware(app)

app.include_router(api_router, prefix='/api/v1', tags=['v1'])


@app.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')
