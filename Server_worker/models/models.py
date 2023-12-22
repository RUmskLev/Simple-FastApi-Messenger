from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey

METADATA = MetaData()

messages = Table(
    "messages",
    METADATA,
    Column("id", Integer, primary_key=True),
    Column("author", Integer, ForeignKey("users.id")),
    Column("recipient", Integer, ForeignKey("users.id")),
    Column("text", String, nullable=False),
    Column("time", TIMESTAMP, default=datetime.utcnow),
)

users = Table(
    "users",
    METADATA,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("last_received", Integer, ForeignKey("messages.id")),
)
