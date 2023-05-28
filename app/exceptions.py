from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

subscribtion_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not subscribed to the channel",
    headers={"WWW-Authenticate": "Bearer"},
)


subscribtion_exception_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Subscribtion not found",
)

content_unit_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Content Unit not found",
)

channel_acces = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No channel access",
)

channel_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Channel not found",
)

not_found_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found",
)
