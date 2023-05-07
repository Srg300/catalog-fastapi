from typing import List, Optional, Type
import enum

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Integer,
    Float,
    SmallInteger,
    MetaData,
    String,
    Table,
    Text,
    ForeignKey,
    Enum,
    desc,
    func
)
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from db import async_session
from models.base import Base
from models.user import User

metadata = MetaData()


class ActivitiesChannel(Base):
    __tablename__ = "cataloging_channel_activities"
    channel_id: Mapped[int] = mapped_column(ForeignKey("cataloging_channel.id"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("cataloging_activity.id"), primary_key=True
    )
    activity: Mapped["Activity"] = relationship(lazy="selectin")


class Activity(Base):
    __tablename__ = 'cataloging_activity'

    title: Mapped[str] = mapped_column('title', String(64), nullable=False)


class ChannelState(str, enum.Enum):
    VALID = 'VALID'
    MODERATION = 'MODERATION'
    BLOCKED = 'BLOCKED'
    INACTIVE = 'INACTIVE'
    DELETED = 'DELETED'


class Channel(Base):
    __tablename__ = 'cataloging_channel'

    title: Mapped[str] = mapped_column('title', String(100), nullable=False)
    slug: Mapped[str] = mapped_column('slug', String(100), unique=True)
    mascot: Mapped[str] = mapped_column('mascot', String(100))
    banner: Mapped[str] = mapped_column('banner', String(100))
    description: Mapped[str] = mapped_column('description', Text(1000))
    channel_rating: Mapped[float] = mapped_column('channel_rating', Float)
    state: Mapped[str] = mapped_column('state', Enum(ChannelState), default=ChannelState.MODERATION)
    is_donation_active: Mapped[bool] = mapped_column(
        'is_donation_active', Boolean, default=False
    )
    created_at: Mapped[str] = mapped_column('created_at', Date)

    owner_id: Mapped[int] = mapped_column(
        "owner_id", ForeignKey("identity_appuser.id"), nullable=False
    )
    owner: Mapped[User] = relationship(lazy="selectin")

    activities: Mapped[List['ActivitiesChannel']] = relationship(lazy="selectin")

    @classmethod
    async def all(cls, skip: int, limit: int):
        stmt = select(cls).options(selectinload(cls.owner))
        stmt = stmt.offset(skip).limit(limit)
        async with async_session() as session:
            res = await session.execute(stmt)
            return res.scalars()

    @classmethod
    async def get(cls, value: int | str):
        """Получить канал по id или slug

        :param value: id: int, slug: str
        :return: Channel
        """

        if isinstance(value, int):
            stmt = select(cls).options(selectinload(cls.owner)).where(cls.id==value)

        if isinstance(value, str):
            stmt = select(cls).options(selectinload(cls.owner)).where(cls.slug==value)

        async with async_session() as session:
            res = await session.execute(stmt)
            return res.one_or_none()
