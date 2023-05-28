
import random
from typing import List, Union

from fastapi import APIRouter, Depends, Query


from schemas.channel import ChannelSimple, Activitie, CreateActivitie

from models.channel import Channel, Activity

from auth import get_current_user
from exceptions import not_found_404, channel_404

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


@router.get("/activities/", response_model=List[Activitie], tags=['channels'])
async def read_all_activity(
        skip: int = 0,
        limit: int | None = None
):
    """ Возвращет все активности
    """

    activities = await Activity.all(skip, limit)
    res = [Activitie.from_orm(activity) for activity in activities]
    return res


@router.post("/activities/", tags=['channels'])
async def create_activity(data: CreateActivitie):
    """ Создает активность
    """
    activity = await Activity.create(data)
    return Activitie.from_orm(*activity)


@router.get("/activities/activity/{id}", response_model=Activitie, tags=['channels'])
async def read_activity(id: int):
    """ Возвращет активность по id
    """

    activity = await Activity.get(id)
    if not activity:
        raise not_found_404
    return Activitie.from_orm(*activity)


@router.put("/activities/activity/{id}", response_model=Activitie, tags=['channels'])
async def update_activity(id: int, data: CreateActivitie):
    """ Возвращет активность по id
    """

    activity = await Activity.update(id, data)
    if not activity:
        raise not_found_404
    return Activitie.from_orm(*activity)


@router.delete("/activities/activity/{id}", tags=['channels'], status_code=202)
async def delete_activity(id: int):
    """ Удаляет активность по id
    """
    activity = await Activity.get(id)
    if not activity:
        raise not_found_404
    await Activity.delete(id)
    return {'msg': 'deleted'}
