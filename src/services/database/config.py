import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.data.settings import POSTGRESQL_URI

_logger = logging.getLogger(__name__)

engine = create_async_engine(POSTGRESQL_URI)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
