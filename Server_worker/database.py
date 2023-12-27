from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from hashing import get_password_hash
from config import (
    DATABASE_HOST,
    DATABASE_PASSWORD,
    DATABASE_USER,
    DATABASE_NAME,
    DATABASE_PORT,
)
from exceptions import (
    UsernameTaken,
    NoMessages,
    NoUser,
    MessageInsertionError,
    HashMismatchError,
)
from exceptions import UsernameTaken, NoRecipient, NoMessages, NoUser
import datetime


"""
This module is responsible for executing database queries.
Fully async and uses async engine for remote connections. Doesn't close after commit.
"""


ENGINE = create_async_engine(
    url=f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    echo=False,
)


AsyncSessionLocal = sessionmaker(ENGINE, expire_on_commit=False, class_=AsyncSession)


async def get_all_messages(user_username: str):
    """
    Collects all messages sent by or sent to user with given username.

    :param user_username: user's username.
    :return: Returns list of messages or raises exception if error occurs.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text(
                "SELECT u1.username AS author_username, u2.username AS recipient_username, m.text AS message_text, m.time AS message_time FROM messages m JOIN users u1 ON m.author = u1.id JOIN users u2 ON m.recipient = u2.id WHERE u1.username = :username OR u2.username = :username"
            ),
            {"username": user_username},
        )
        messages = result.all()
        if not messages:
            raise NoMessages("No messages found for this user.")
        if messages is not None:
            return messages
        return []


async def get_last_messages(user_username: str, provided_hash: str):
    """
    Checks hash of last message that user has and that server has. Collects all messages after message with id in "last received" user's column. Updates last_received message.

    :param user_username: user's username.
    :param provided_hash: user's last message hash.
    :return: Returns list of collected messages on success, otherwise raises an error.
    """
    async with AsyncSessionLocal() as session:
        cursor = await session.execute(
            text("SELECT * FROM messages WHERE id = (SELECT last_received FROM users WHERE username = :username)"),
            {"username": user_username},
        )
        last_received_message = cursor.fetchone()
        if last_received_message is not None:
            print("weweewewewewewewe")
            last_message_serialized = "|".join(str(last_received_message[i]) for i in range(len(last_received_message)))
            last_received_id = last_received_message[0]
        else:
            print("owowowowoowowo")
            last_received_id = 1
            await session.execute(
                text("UPDATE users SET last_received = :last_received_id WHERE username = :username"),
                {"last_received_id": last_received_id, "username": user_username},
            )
            await session.commit()
            return await get_all_messages(user_username)

        message_hash = await get_password_hash(last_message_serialized)
        if message_hash != provided_hash:
            raise HashMismatchError()

        messages = await get_all_messages(user_username)

        if not messages:
            last_received_id = 1
        else:
            last_received_id = messages[-1][0]

        await session.execute(
            text("UPDATE users SET last_received = :last_received_id WHERE username = :username"),
            {"last_received_id": last_received_id, "username": user_username},
        )

        await session.commit()

        return messages


async def new_message(author: str, recipient: str, message_text: str):
    """
    Saves new message to database.

    :param author: username of user, that sent message.
    :param recipient: username of user, that received message.
    :param message_text: text of message.
    :return: Returns None on success, otherwise raises an error.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": recipient},
        )
        user = result.fetchone()
        if user is None:
            raise NoRecipient(f"No user with username {recipient} found.")
        else:
            await session.execute(
                text(
                    "INSERT INTO messages (author, recipient, text, time) VALUES ((SELECT id FROM users WHERE username = :author), (SELECT id FROM users WHERE username = :recipient), :message_text, :current_time)"
                ),
                {
                    "author": author,
                    "recipient": recipient,
                    "message_text": message_text,
                    "current_time": datetime.datetime.utcnow(),
                },
            )
            await session.commit()


async def new_user(username: str, hashed_password: str):
    """
    Saves new user to database.

    :param username: new user's username.
    :param hashed_password: new user's hashed password.
    :return: Returns None on success, otherwise raises an error.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username},
        )
        user = result.fetchone()
        if user is not None:
            raise UsernameTaken()
        else:
            await session.execute(
                text(
                    "INSERT INTO users (username, hashed_password, registered_at) VALUES (:username, :hashed_password, :current_time)"
                ),
                {
                    "username": username,
                    "hashed_password": hashed_password,
                    "current_time": datetime.datetime.utcnow(),
                },
            )
            await session.commit()


async def get_user_by_username(user_username: str):
    """
    Returns data of user with given username.

    :param user_username: user's username.
    :return: Returns Row on success or raises an error, if no user found.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT username, hashed_password FROM users WHERE username = :username"),
            {"username": user_username},
        )
        user = result.fetchone()
        if user is None:
            raise NoUser()
        return user
