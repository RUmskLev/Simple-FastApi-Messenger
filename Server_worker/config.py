import os
from dotenv import load_dotenv


"""
Loads sensitive data to OS variables from .env file.
"""


load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
HASHING_ALGORYTHM = os.getenv("HASHING_ALGORYTHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT")
