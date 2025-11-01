from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import Settings


# URL debe ser async driver, p.ej. "mysql+asyncmy://user:pass@host/db" o "postgresql+asyncpg://..."
DATABASE_URL = Settings.MYSQL_DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_sql_db():
    # importa modelos que hereden de SQLModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)