from typing import Union, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int


class UserOut(UserBase):
    username: str
    email: Optional[str]
    picture: str
    is_active: bool
    is_registered: bool
    phone: Optional[str]
    is_phone_confirmed: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserInfo(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    picture: str
    slug: Optional[str]
    title: Optional[str]


class UserInfoForChannel(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    picture: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[int, None] = None


class AnonymousUser(BaseModel):
    id: None = None
