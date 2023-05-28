import enum
from typing import List

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    MetaData,
    String,
    Text,
    ForeignKey,
    Enum,
)
from sqlalchemy import select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from pytils.translit import slugify

from models.base import Base
from models.user import User
from schemas.channel import CreateActivitie

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
    slug: Mapped[str] = mapped_column('slug', String(50), nullable=False)

    @classmethod
    async def create(cls, data: CreateActivitie):
        _data = data.dict()
        _data['slug'] = slugify(data.title)
        slug = slugify(data.title)
        activitie = Activity(**_data)
        async with cls.async_session as session:
            session.add(activitie)
            await session.commit()
            new = await cls.get(activitie.id)
            if not new:
                raise RuntimeError()
            return new

    @classmethod
    async def update(cls, id: int, data: CreateActivitie):
        data = data.dict()
        if isinstance(id, int):
            stmt = update(cls).where(cls.id==id).values(title=data['title'])
        async with cls.async_session as session:
            await session.execute(stmt)
            await session.commit()
            res = await cls.get(id)
            return res


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
        async with cls.async_session as session:
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

        async with cls.async_session as session:
            res = await session.execute(stmt)
            return res.one_or_none()
