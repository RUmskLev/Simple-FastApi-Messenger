from passlib.context import CryptContext


"""
This module provides ability to hash text and verify given hash and hash generated from text. Algorythm can be chosen by application.
"""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if given hash is the same as hashed given text.

    :param plain_password: text to hash and compare.
    :param hashed_password: hashed text to compare.
    :return bool: Returns True if hashes are the same, otherwise returns False.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """
    Hashes given text and returns hash.

    :param password: text to hash.
    :return str: Returns generated hash.
    """
    return pwd_context.hash(password)
