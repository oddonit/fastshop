from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import (
    SQLModel,
    create_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from src.base_settings import base_settings


engine = AsyncEngine(create_engine(base_settings.postgres.url, echo=True, future=True))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
