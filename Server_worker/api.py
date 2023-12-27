from pydantic import BaseModel
from starlette.requests import Request
from exceptions import (
    NoMessages,
    UsernameTaken,
    NoRecipient,
)
from hashing import get_password_hash
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth import (
    create_access_token,
    Token,
    User,
    get_current_active_user,
    authenticate_user,
    OAuth2PasswordRequestFormUser,
)
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from database import get_all_messages, new_message, new_user, get_last_messages
from loadup import ConnectedUser, get_users_amount
from loguru import logger


"""
Module, that runs API on uvicorn server. Receives all outbound requests. 
"""


app = FastAPI(title="Worker server")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ServerModel(BaseModel):
    """
    Pydantic model, that describes server's credentials.
    """

    address: str | None = None
    port: int | None = None
    error: str | None = None


class MessagesModel(BaseModel):
    """
    Pydantic model, that describes return on /message_history request.
    """

    result: str
    messages: list | None = None
    error: str | None = None


class BoolResponseModel(BaseModel):
    """
    Pydantic model, that describes boolean return.
    """

    result: str


class LastMessageModel(BaseModel):
    """
    Pydantic model, that describes return on /check_for_updates request.
    """

    result: str
    last_message_hash: str | None = None
    error: str | None = None


class LoadupModel(BaseModel):
    """
    Pydantic model, that describes return on /loadup request.
    """

    users_amount: int


class Message(BaseModel):
    """
    Pydantic model, that describes request for /new_message request.
    """

    message_text: str
    recipient_username: str


#
# Worker server to user
#


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestFormUser, Depends()]):
    """
    Handler for /token request.

    :param form_data: json body with user's credentials.
    :return: Returns result of request.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    ConnectedUser(form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/send_message", response_model=BoolResponseModel)
@limiter.limit("3/second")
async def send_message(
    request: Request, current_user: Annotated[User, Depends(get_current_active_user)], message: Message
):
    """
    Handler for /send_message request.

    :param request: parameter used by limiter only for limit amount of requests.
    :param current_user: user's credentials.
    :param message: text of the message.
    :return: Returns result of request.
    """
    logger.info(f"{current_user, message.message_text, message.recipient_username}")
    try:
        await new_message(current_user.username, message.recipient_username, message.message_text)
    except NoRecipient:
        return {"result": "error", "error": "There is no user with given username!"}
    return {"result": "success"}


@app.get("/message_history", response_model=MessagesModel)
async def message_history(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Handler for /message_history request.

    :param request: parameter used by limiter only for limit amount of requests.
    :param current_user: user's credentials.
    :return: Returns result of request.
    """
    try:
        messages = [tuple(message) for message in await get_all_messages(current_user.username)]
        return {"result": "success", "messages": messages}
    except NoMessages:
        return {"result": "error", "error": "No messages found"}


@app.get("/check_for_updates", response_model=MessagesModel)
@limiter.limit("1/second")
async def check_for_updates(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    last_message_hash: str,
):
    """
    Handler for /check_for_updates request.

    :param request: parameter used by limiter only for limit amount of requests.
    :param current_user: user's credentials.
    :param last_message_hash:
    :return: Returns result of request.
    """
    print(current_user, last_message_hash)
    try:
        last_messages = await get_last_messages(current_user.username, last_message_hash)
        return {"result": "success", "last_messages": [tuple(mes) for mes in last_messages]}
    except Exception:
        return {"result": "error", "error": "No messages found"}


@app.post("/register", response_model=BoolResponseModel)
@limiter.limit("5/minute")
async def register(request: Request, user_username: str, user_password: str):
    """
    Handler for /register request.

    :param request: parameter used by limiter only for limit amount of requests.
    :param user_username: user's username.
    :param user_password: user's password.
    :return: Returns result of request.
    """
    hashed_password = await get_password_hash(user_password)
    try:
        await new_user(user_username, hashed_password)
    except UsernameTaken:
        return {"result": "error", "error": "This username is already taken!"}
    return {"result": "success"}


@app.get("/loadup", response_model=LoadupModel)
async def loadup():
    """
    Handler for /loadup request.

    :return: Returns result of request.
    """
    return {"users_amount": await get_users_amount()}
