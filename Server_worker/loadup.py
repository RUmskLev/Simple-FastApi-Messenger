import asyncio
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta


"""
This module is used to control and check active users and to represent server's loadup.
"""


class ConnectedUser:
    """
    Class for connected users. Has builtin methods to check user's token availability.
    """

    def __init__(self, username):
        self.connection_time = datetime.utcnow()
        self.username = username
        self.update_users_list()

    def __repr__(self):
        return f"{self.username=} | {self.connection_time=}"

    def is_token_expired(self) -> bool:
        """
        Checks if token expired.

        :return: Returns True if expired, otherwise returns False.
        """
        if self.connection_time < datetime.utcnow() - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
            return True
        return False

    def update_users_list(self) -> None:
        """
        Writes itself to list of active users if it is active and not presented in list.

        :return: Returns None.
        """
        for user in users:
            if user.username == self.username:
                return
        users.append(self)


users = []
users_amount = 0


async def update_connected() -> None:
    """
    Updates list of active users. Checks activity for every user.

    :return: Returns None.
    """
    global users_amount, users
    cur_users_connected = 0
    for user in users:
        if not user.is_token_expired():
            cur_users_connected += 1
        else:
            users.remove(user)
    users_amount = cur_users_connected


async def get_users_amount() -> int:
    """
    Calculates amount of active users.

    :return int: Returns total amount
    """
    await update_connected()
    return users_amount
