from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)

from src.base_settings import base_settings
from src.users.models.database import User
from src.users.services import get_user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(
    service: Annotated[get_user_service, Depends()],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, base_settings.auth.secret_key, algorithms=[base_settings.auth.algorithm])
        pk: int = payload.get('sub')
        if pk is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.detail(pk=int(pk))

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
