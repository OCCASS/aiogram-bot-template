from .models import db
from src.data.config import POSTGRESQL_URI


async def create_database():
    await db.set_bind(POSTGRESQL_URI)
    await db.gino.create_all()
