from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from schemas.user import UserOut, TokenData, AnonymousUser
from models.user import User
from exceptions import credentials_exception

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(id: int):
    """ Получение пользователя по id """
    user = await User.get(id)
    return UserOut.from_orm(*user)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_user(id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return await user
