from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, delete
from sqlalchemy.orm import Mapped, mapped_column, selectinload

from db import async_session


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=convention)
    async_session = async_session()

    id: Mapped[int] = mapped_column(
        'id', autoincrement=True, nullable=False, unique=True, primary_key=True
    )

    def __repr__(self) -> str:
        columns = ", ".join(
            [f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"<{self.__class__.__name__}({columns})>"

    @classmethod
    async def get(cls, id: int):
        if isinstance(id, int):
            stmt = select(cls).where(cls.id==id)
        async with cls.async_session as session:
            res = await session.execute(stmt)
            return res.one_or_none()

    @classmethod
    async def delete(cls, id: int):
        if isinstance(id, int):
            stmt = delete(cls).where(cls.id==id)
        async with cls.async_session as session:
            await session.execute(stmt)
            await session.commit()
            return None

    @classmethod
    async def all(cls, skip: int, limit: int):
        stmt = select(cls).offset(skip).limit(limit)
        async with cls.async_session as session:
            res = await session.execute(stmt)
            return res.scalars()
