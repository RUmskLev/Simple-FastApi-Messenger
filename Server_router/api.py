from pydantic import BaseModel
from starlette.requests import Request
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth import create_access_token, authenticate_server, Token, Servers_workers, OAuth2PasswordRequestFormServer
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


Active_workers = []


app = FastAPI(title="Router server")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ServerModel(BaseModel):
    address: str | None = None
    port: int | None = None
    error: str | None = None


#
# User to server
#


@app.get("/get_worker_address", response_model=ServerModel)
@limiter.limit("2/second")
async def return_less_loaded_worker(request: Request):
    if len(Active_workers) > 0:
        return {"status": 200, "address": Active_workers[0][0], "port": Active_workers[0][1]}
    else:
        return {"status": 200, "error": "No servers are available now"}
