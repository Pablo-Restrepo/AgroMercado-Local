from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

# URL debe ser async driver, p.ej. "mysql+asyncmy://user:pass@host/db" o "postgresql+asyncpg://..."
DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    # importa modelos que hereden de SQLModel
    from infraestructure.db.modelsSQL import CompraModel, ProductoModel, ProductoUnitarioModel, EnvioModel, UsuarioModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def close_db():
    """Cerrar/disponer el engine async y sus pools antes de que se cierre el event loop."""
    try:
        await engine.dispose()
    except Exception:        
        pass