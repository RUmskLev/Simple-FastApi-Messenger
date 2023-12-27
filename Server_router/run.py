from loguru import logger
import uvicorn
from api import app
from config import SERVER_HOST, SERVER_PORT


"""
Run this to start the server. Makes logs and start uvicorn server with given SERVER_HOST and SERVER_PORT.
You can specify it in .env file (Check .env.example).

Logs are saved in ./logs.
"""


def main():
    """
    Main function of app. Starts uvicorn server.
    :return: None
    """
    logger.remove()
    logger.add("logs/debug_{time}.log", rotation="00:00", compression="zip", enqueue=True, colorize=True)
    logger.info("Start of application")

    logger.level("API", no=110, color="<blue>")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)


if __name__ == "__main__":
    """
    Entry point of server application.
    """
    main()
