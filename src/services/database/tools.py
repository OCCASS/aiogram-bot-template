import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.database.config import async_session

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def session_scope() -> AsyncSession:
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        _logger.error("session scope error: {}".format(e))
        await session.rollback()
        raise
    finally:
        await session.close()
