#
# Run this to start the server
#
import asyncio
from loadup import update_connected
from loguru import logger
import uvicorn
from api import app
from config import SERVER_HOST, SERVER_PORT


def main():
    logger.remove()
    logger.add("logs/debug_{time}.log", rotation="00:00", compression="zip", enqueue=True, colorize=True)
    logger.info("Start of application")

    logger.level("API", no=110, color="<blue>")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, loop="asyncio")


if __name__ == '__main__':
    main()
