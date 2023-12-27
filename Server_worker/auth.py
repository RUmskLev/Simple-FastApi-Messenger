from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from hashing import verify_password
from config import JWT_SECRET_KEY, HASHING_ALGORYTHM
from database import get_user_by_username


"""
Module that is responsible for authentication. Creates and checks JWT tokens.
"""


class OAuth2PasswordRequestFormUser:
    """
    Custom request form. Stores credentials, that user should provide.
    """

    def __init__(
        self,
        *,
        username: Annotated[
            str,
            Form(),
        ],
        password: Annotated[
            str,
            Form(),
        ],
    ):
        self.username = username
        self.password = password


class Token(BaseModel):
    """
    Pydantic model, describes Token's structure.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Pydantic model, describes full Token's data.
    """

    username: str | None = None


class User(BaseModel):
    """
    Pydantic model, describes User's data
    """

    username: str
    disabled: bool | None = None


class UserInDB(User):
    """
    Pydantic model, describes User with hashed password.
    """

    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(username: str):
    """
    Receives user's data by searching him in database.

    :param username: user's username
    :return: Returns pydantic UserInDB model if user found, otherwise returns error message.
    """
    result = await get_user_by_username(username)
    return UserInDB(**{"username": result[0], "hashed_password": result[1]})


async def authenticate_user(username: str, password: str):
    """
    Checks if user with given credentials exists in database and checks its password.

    :param username: user's username
    :param password: user's password
    :return: Returns pydantic UserInDB model on success, otherwise returns error message or raises an error.
    """
    user = await get_user(username)
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates JWT access token for user.

    :param data: User's credentials, that will be encoded.
    :param expires_delta: Time at which JWT token works.
    :return: Returns Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=HASHING_ALGORYTHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    It gets user's token and checks its validity.

    :param token: given JWT token
    :return: Returns user's data if token is right, otherwise raises an error.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[HASHING_ALGORYTHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Makes full loop of checks for user and checks if user is disabled.

    :param current_user: User pydantic model, which has user's credentials.
    :return: Returns User on success, otherwise raises HTTPException with code 400 (Inactive user)
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
