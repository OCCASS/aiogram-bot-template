from typing import Generator
from typing import Self
from typing import Sequence

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import DeclarativeBase

from src.services.database.tools import session_scope


class Model(DeclarativeBase):
    @classmethod
    async def all(cls) -> Sequence[Self]:
        async with session_scope() as session:
            q = select(cls)
            instances = await session.execute(q)
            instances = instances.scalars()

        return instances.fetchall()

    @classmethod
    async def filter_by(cls, **kwargs) -> Sequence[Self]:
        async with session_scope() as session:
            q = select(cls).filter_by(**kwargs)
            instances = await session.execute(q)
            instances = instances.scalars()

        return instances.fetchall()

    @classmethod
    async def filter(cls, *criteria) -> Sequence[Self]:
        async with session_scope() as session:
            q = select(cls).filter(*criteria)
            instances = await session.execute(q)
            instances = instances.scalars()

        return instances.fetchall()

    @classmethod
    async def create(cls, **kwargs) -> Self:
        async with session_scope() as session:
            instance = cls(**kwargs)
            session.add(instance)

        return instance

    @classmethod
    async def get(cls, **kwargs) -> Self:
        async with session_scope() as session:
            q = select(cls).filter_by(**kwargs)
            instances = await session.execute(q)
            instance = instances.first()

        return instance if instance is None else instance[0]

    @classmethod
    async def get_or_create(cls, **kwargs) -> tuple[Self, bool]:
        if instance := await cls.get(**kwargs):
            return instance, False
        else:
            instance = await cls.create(**kwargs)
            return instance, True

    async def update(self, **new_values) -> None:
        new_values = self._filter_new_values(new_values)
        async with session_scope() as session:
            unset_values = {k: getattr(self, k) for k in self.columns if k not in new_values}
            q = update(self.__class__).values(**new_values).filter_by(**unset_values)
            await session.execute(q)

        for key, value in new_values.items():
            setattr(self, key, value)

    async def delete(self) -> None:
        async with session_scope() as session:
            await session.delete(self)

    @property
    def columns(self) -> Generator[str, str, None]:
        return (c.key for c in self.__table__.columns)

    def _filter_new_values(self, new_value: dict):
        return {k: v for k, v in new_value.items() if k in self.columns}
