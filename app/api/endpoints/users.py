from fastapi import APIRouter, Depends

from schemas.user import UserOut

from models.channel import Channel
from models.user import User


from auth import get_current_user
from exceptions import credentials_exception

router = APIRouter()


@router.get("/users/{id}/", response_model=UserOut, tags=['users'])
async def get_user_(id: int):
    """ Получение пользователя по id jwt token """

    user = await User.get(id)
    if user:
        return UserOut.from_orm(*user)
    raise credentials_exception


@router.get("/users/user/{id}/", response_model=UserOut, tags=['users'])
async def get_user(id: int, current_user: UserOut = Depends(get_current_user)):
    """ Получение пользователя по id jwt token """

    user = await User.get(id)
    if user.id == current_user.get('id'):
        return UserOut.from_orm(*user)
    raise credentials_exception


@router.get("/users/me/", response_model=UserOut, tags=['users'])
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    """ Возвращает текущего пользователя по токену """

    channel = await Channel.get_by_user(current_user.get('id'))
    if channel:
        current_user['channel'] = channel
    data = UserOut(**current_user)
    return data
