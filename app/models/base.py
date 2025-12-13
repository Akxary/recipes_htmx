import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from resources.config import A_DB_URL, DB_URL

logger = logging.getLogger(__name__)
a_engine = create_async_engine(A_DB_URL)
engine = create_engine(DB_URL)
async_session = async_sessionmaker(
    a_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_fapi_db() -> AsyncGenerator[AsyncSession, Any]:
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        logger.exception("Postgresql database connection error: %s", e)
        raise
