from datetime import datetime, timedelta
from typing import Annotated
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from config import JWT_SECRET_KEY, HASHING_ALGORYTHM


# For testing purposes only, don't use in production. Password for "worker" is "secret"
Servers_workers = {
    "worker": {
        "servername": "worker",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str | None = None
    token_type: str | None = None
    error: str | None = None


class TokenData(BaseModel):
    username: str | None = None


class Server(BaseModel):
    servername: str
    disabled: bool | None = None


class ServerInDB(Server):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class OAuth2PasswordRequestFormServer:
    def __init__(
        self,
        *,
        servername: Annotated[
            str,
            Form(),
        ],
        password: Annotated[
            str,
            Form(),
        ],
        working_ip: Annotated[
            str,
            Form(),
        ],
        working_port: Annotated[
            int,
            Form(),
        ],
    ):
        self.servername = servername
        self.password = password
        self.working_ip = working_ip
        self.working_port = working_port


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_server(db, servername: str):
    if servername in db:
        user_dict = db[servername]
        return ServerInDB(**user_dict)


def authenticate_server(fake_db, servername: str, password: str):
    server = get_server(fake_db, servername)
    if not server:
        return False
    if not verify_password(password, server.hashed_password):
        return False
    return server


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=HASHING_ALGORYTHM)
    return encoded_jwt
