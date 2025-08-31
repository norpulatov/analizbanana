from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)

class Base(DeclarativeBase):
    pass

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    from src import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
