from pydantic import BaseModel
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth import create_access_token, authenticate_server, Token, Servers_workers, OAuth2PasswordRequestFormCustom
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated


Active_workers = []


app = FastAPI(title="Router server")


class ServerModel(BaseModel):
    address: str | None = None
    port: int | None = None
    details: str | None = None


#
# User to server
#


@app.get("/get_worker_address", response_model=ServerModel)
async def return_less_loaded_worker():
    if len(Active_workers) > 0:
        return {"status": 200, "address": Active_workers[0][0], "port": Active_workers[0][1], "details": "Success"}
    else:
        return {"status": 200, "details": "No servers are available now"}


#
# Worker server to router server
#


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestFormCustom, Depends()]):
    server = authenticate_server(Servers_workers, form_data.servername, form_data.password)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect servername or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": server.servername}, expires_delta=access_token_expires)
    Active_workers.append((form_data.working_ip, form_data.working_port))
    return {"access_token": access_token, "token_type": "bearer"}
