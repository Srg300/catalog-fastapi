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


user_model = Table(
    "identity_appuser",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(150), unique=True),
    Column("first_name", String()),
    Column("last_name", String()),
    Column("email", String(254), unique=True),
    Column("phone", String(254), unique=True),
    Column("picture", String(100), nullable=True),
    Column("is_active", Boolean),
    Column("is_registered", Boolean),
    Column("is_phone_confirmed", Boolean),
)


class UserModel:
    @classmethod
    async def get(cls, id: int):
        # pass
        query = user_model.select().where(user_model.c.id == id)
        return await db_session.fetch_one(query)

    @classmethod
    async def all(cls):
        query = user_model.select()
        return await db_session.fetch_all(query=query)

    @classmethod
    async def get_subscribtions(cls, id: int):
        """ Список активных подписок пользователя """
        query = s.subscriber.select().where(
            (s.subscriber.c.owner_id == id) &
            (s.subscriber.c.subscription_state == 'valid')
        ).distinct()
        user_subscribe = await db_session.fetch_all(query)
        return user_subscribe

    @classmethod
    async def get_subscribtions_list_id(cls, id: int):
        """ Список id активных подписок пользователя """
        query = s.subscriber.select().where(
            (s.subscriber.c.owner_id == id) &
            (s.subscriber.c.subscription_state == 'valid')
        ).distinct()
        subscription_list = []
        async for sub in db_session.iterate(query=query):
            subscription_list.append(sub._mapping['subscription_id'])
        return subscription_list

    @classmethod
    async def get_by_subscription(cls, sub_id: int):
        query = user_model.select().join(
            s.subscriber, s.subscriber.c.owner_id == user_model.c.id
        ).where(s.subscriber.c.id == sub_id)
        user = await db_session.fetch_one(query=query)
        return user
