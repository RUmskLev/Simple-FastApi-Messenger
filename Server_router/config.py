import os
from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
HASHING_ALGORYTHM = os.getenv("HASHING_ALGORYTHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
