from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from Server_worker.hashing import get_password_hash
from config import DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USER, DATABASE_NAME, DATABASE_PORT
from exceptions import UsernameTaken, NoMessages, NoUser, MessageInsertionError, HashMismatchError
import datetime


ENGINE = create_async_engine(
    url=f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    echo=True,
)


AsyncSessionLocal = sessionmaker(ENGINE, expire_on_commit=False, class_=AsyncSession)


async def get_all_messages(user_username: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT u1.username AS author_username, u2.username AS recipient_username, m.text AS message_text, m.time AS message_time FROM messages m JOIN users u1 ON m.author = u1.id JOIN users u2 ON m.recipient = u2.id WHERE u1.username = :username OR u2.username = :username"), {"username": user_username})
        messages = result.all()
        if not messages:
            raise NoMessages("No messages found for this user.")
        return messages


async def get_last_messages(user_username: str, provided_hash: str):
    async with AsyncSessionLocal() as session:
        cursor = await session.execute(text("SELECT * FROM messages WHERE id = (SELECT last_sent FROM users WHERE username = :username)"), {"username": user_username})
        last_received_message = cursor.fetchone()
        last_message_serialized = "|".join(str(last_received_message[i]) for i in range(len(last_received_message)))
        last_received_id = last_received_message[0]
        message_hash = await get_password_hash(last_message_serialized)
        if message_hash != provided_hash:
            raise HashMismatchError()

        query = text("SELECT u1.username AS author_username, u2.username AS recipient_username, m.text AS message_text, m.time AS message_time FROM messages m JOIN users u1 ON m.author = u1.id JOIN users u2 ON m.recipient = u2.id WHERE (u1.username = :username OR u2.username = :username) AND m.id > :last_sent_id ORDER BY m.time DESC")
        result = await session.execute(query, {"username": user_username, "last_sent_id": last_received_id})
        messages = result.fetchall()

        if not messages:
            raise NoMessages()

        return messages


async def new_message(author: str, recipient: str, message_text: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("INSERT INTO messages (author, recipient, text, time) VALUES ((SELECT id FROM users WHERE username = :author), (SELECT id FROM users WHERE username = :recipient), :message_text, :current_time) RETURNING id"), {"author": author, "recipient": recipient, "message_text": message_text, "current_time": datetime.datetime.utcnow()})
        message_id = result.fetchone()[0]
        if message_id is None:
            raise MessageInsertionError()


async def new_user(username: str, hashed_password: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username})
        user = result.fetchone()
        if user is not None:
            raise UsernameTaken()
        else:
            await session.execute(text("INSERT INTO users (username, hashed_password, registered_at) VALUES (:username, :hashed_password, :current_time)"), {"username": username, "hashed_password": hashed_password, "current_time": datetime.datetime.utcnow()})
            await session.commit()


async def get_user_by_username(user_username: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT username, hashed_password FROM users WHERE username = :username"), {"username": user_username})
        user = result.fetchone()
        if user is None:
            raise NoUser()
        return user
