from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.sql import select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from db import async_session


metadata = MetaData()


class User(Base):
    __tablename__ = 'identity_appuser'

    username: Mapped[str] = mapped_column('username', String(100), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column('first_name', String(100))
    last_name: Mapped[str] = mapped_column('last_name', String(100))
    email: Mapped[str] = mapped_column('email', String(254), unique=True)
    phone: Mapped[str] = mapped_column('phone', String(254), unique=True)
    picture: Mapped[str] = mapped_column('picture', String(100))
    is_active: Mapped[bool] = mapped_column('is_active', Boolean)
    is_registered: Mapped[bool] = mapped_column('is_registered', Boolean)
    is_phone_confirmed: Mapped[bool] = mapped_column('is_phone_confirmed', Boolean)

    @classmethod
    async def get(cls, id: int):
        """Получить пользователя по id

        :param id: int
        :return: User
        """
        stmt = select(cls).where(cls.id==id)

        async with async_session() as session:
            res = await session.execute(stmt)
            return res.one_or_none()
