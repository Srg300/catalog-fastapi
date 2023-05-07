from datetime import date
from typing import Optional, List, Any
from enum import Enum

from pydantic import BaseModel
from .user import UserInfoForChannel, UserOut


class ChannelSort(str, Enum):
    id = "id"
    random = "random"



class Activitie(BaseModel):
    title: str

    class Config:
        orm_mode = True


class Activities(BaseModel):
    activity: Activitie

    class Config:
        orm_mode = True


class ChannelBase(BaseModel):
    id: int


class ChannelSimple(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)
        self.activities = [i.activity.title for i in self.activities]

    id: int
    title: str
    slug: str
    description: str
    mascot: str
    banner: str
    state: str
    is_donation_active: bool
    created_at: date
    owner_id: int | None
    owner: Optional[UserInfoForChannel]
    activities: Optional[List[Activities]]

    class Config:
        orm_mode = True
