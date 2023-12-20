import asyncio
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta


class ConnectedUser:
    def __init__(self, username):
        self.connection_time = datetime.utcnow()
        self.username = username
        self.update_users_list()

    def __repr__(self):
        return f"{self.username=} | {self.connection_time=}"

    def is_token_expired(self):
        if self.connection_time < datetime.utcnow() - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
            return True
        return False

    def update_users_list(self):
        for user in users:
            if user.username == self.username:
                return
        users.append(self)


users = []
users_amount = 0


async def update_connected():
    global users_amount, users
    cur_users_connected = 0
    for user in users:
        if not user.is_token_expired():
            cur_users_connected += 1
        else:
            users.remove(user)
    users_amount = cur_users_connected


async def get_users_amount():
    await update_connected()
    return users_amount
