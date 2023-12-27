import os
from dotenv import load_dotenv


"""
Loads sensitive data to OS variables from .env file. Also list of active worker servers is listed here.
"""


load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

Active_workers = [["185.229.65.227", 8000, 100]]
