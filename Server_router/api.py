from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Router server")


class ServerModel(BaseModel):
    address: str
    port: int


#
# User to server
#


@app.get("/get_worker_address", response_model=ServerModel)
async def return_less_loaded_worker():
    return {"status": 200, "address": "127.0.0.1", "port": 8000}
