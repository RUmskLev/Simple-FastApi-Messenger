from pydantic import BaseModel
from starlette.requests import Request
from Server_worker.exceptions import NoMessages, UsernameTaken, NoRecipient
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth import create_access_token, Token, User, get_current_active_user, authenticate_user, get_password_hash, OAuth2PasswordRequestFormUser
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from database import get_all_messages, new_message, new_user, get_last_message
from loadup import ConnectedUser, get_users_amount


app = FastAPI(title="Worker server")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ServerModel(BaseModel):
    address: str | None = None
    port: int | None = None
    error: str | None = None


class MessagesModel(BaseModel):
    result: str
    messages: list | None = None
    error: str | None = None


class BoolResponseModel(BaseModel):
    result: str


class LastMessageModel(BaseModel):
    result: str
    last_message_hash: str | None = None
    error: str | None = None


class LoadupModel(BaseModel):
    users_amount: int


#
# Worker server to user
#


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestFormUser, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    ConnectedUser(form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/send_message", response_model=BoolResponseModel)
@limiter.limit("3/second")
async def send_message(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    message_text: str,
    recipient_username: str
):
    try:
        await new_message(current_user.username, recipient_username, message_text)
    except NoRecipient:
        return {"result": "error", "error": "There is no user with given username!"}
    return {"result": "success"}


@app.get("/message_history", response_model=MessagesModel)
async def message_history(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        messages = await get_all_messages(current_user.username)
        messages = [tuple(message) for message in messages]
    except NoMessages:
        return {"result": "error", "error": "No messages found"}
    return {"result": "success", "messages": messages}


@app.get("/check_for_updates", response_model=LastMessageModel)
async def check_for_updates(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        last_message = await get_last_message(current_user.username)
        last_message_serialized = "|".join(str(last_message[i]) for i in range(4))
    except NoMessages:
        return {"result": "error", "error": "No messages found"}
    return {"result": "success", "last_message_hash": await get_password_hash(last_message_serialized)}


@app.post("/register", response_model=BoolResponseModel)
@limiter.limit("2/minute")
async def register(request: Request, user_username: str, user_hashed_password: str):
    hp = await get_password_hash(user_hashed_password)
    try:
        await new_user(user_username, hp)
    except UsernameTaken:
        return {"result": "error", "error": "This username is already taken!"}
    return {"result": "success"}


@app.get("/loadup", response_model=LoadupModel)
async def loadup():
    return {"users_amount": await get_users_amount()}
