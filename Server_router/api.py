from pydantic import BaseModel
from starlette.requests import Request
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import requests
from config import Active_workers


"""
This module is used to process api requests using FastApi.
"""


def loadup():
    """
    Sends request to every listed worker server and sorts it by lowest loadup.
    Worker servers are listed in Active_workers list in config.py.
    If server not responding - it's loadup saved as 100 active users.
    :return: None
    """
    for worker in Active_workers:
        url = f"http://{worker[0]}:{worker[1]}/loadup"
        response = requests.get(url)
        worker[2] = response.json().get("users_amount", 100)
    sorted(Active_workers, key=lambda w: w[2])


app = FastAPI(title="Router server")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ServerModel(BaseModel):
    """
    Pydantic model. Describes expected server return of /get_worker_address request.
    """

    address: str | None = None
    port: int | None = None
    error: str | None = None


#
# User to server
#


@app.get("/get_worker_address", response_model=ServerModel)
@limiter.limit("2/second")
async def return_less_loaded_worker(request: Request):
    """
    Proceeds /get_worker_address request. Checks for less loaded server and returns its address and working port.
    :param request: Request object, used for request limiter.
    :return: ServerModel or error: "No servers are available now" if there is no severs listed in Active_workers.
    """
    if len(Active_workers) > 0:
        loadup()
        return {"status": 200, "address": Active_workers[0][0], "port": Active_workers[0][1]}
    else:
        return {"status": 200, "error": "No servers are available now"}
