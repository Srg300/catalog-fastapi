
import random
from typing import List, Union

from fastapi import APIRouter, Depends, Query


from schemas.channel import ChannelSimple

from models.channel import Channel

from auth import get_current_user
from exceptions import *

router = APIRouter()


@router.get("/channels/", response_model=List[ChannelSimple], tags=['channels'])
async def read_all_channels(
        skip: int = 0,
        limit: int | None = None
):
    """ Возвращет все каналы
    """

    channels = await Channel.all(skip, limit)
    res = [ChannelSimple.from_orm(channel) for channel in channels]
    return res


@router.get("/channels/channel/{ch}", response_model=ChannelSimple, tags=['channels'])
async def read_all_channels(ch: int | str):
    """ Возвращет канал по id или slug
    """

    channel = await Channel.get(ch)
    print(type(channel), channel)
    ch = ChannelSimple.from_orm(*channel)
    if channel is None:
        raise channel_404
    return ChannelSimple.from_orm(*channel)
