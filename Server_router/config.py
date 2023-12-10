import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
logger.info("Loaded environment variables")

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
