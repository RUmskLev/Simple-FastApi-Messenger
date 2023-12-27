import os
from dotenv import load_dotenv


"""
Loads sensitive data to OS variables from .env file.
"""


load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
