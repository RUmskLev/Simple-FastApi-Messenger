import random
import pytest
from exceptions import NoUser, UsernameTaken
from hashing import verify_password, get_password_hash
from database import get_user_by_username, AsyncSessionLocal, new_user


@pytest.mark.asyncio
async def test_verify_password():
    plain_password = "right_password"
    hashed_password = await get_password_hash("right_password")
    result = await verify_password(plain_password, hashed_password)
    assert result == True


@pytest.mark.asyncio
async def test_verify_password_fail():
    plain_password = "wrong_password"
    hashed_password = await get_password_hash("right_password")
    result = await verify_password(plain_password, hashed_password)
    assert result == False


@pytest.mark.asyncio
async def test_hashed_different():
    password = "right_password"
    hashed_password = await get_password_hash(password)
    print(hashed_password)
    assert hashed_password != await get_password_hash("right_password")


@pytest.mark.asyncio
async def test_database():
    async with AsyncSessionLocal():

        # get user that exists
        result = await get_user_by_username("test_user")
        assert result is not None

        # get user that doesn't exist
        with pytest.raises(NoUser):
            await get_user_by_username("test_user_doesnt_exists")

        # new user that already exists
        with pytest.raises(UsernameTaken):
            await new_user("test_user", "abc")

        # new user that is not in table
        random_username = ''.join(random.choice("qwersdfiau23897") for _ in range(15))
        result = await new_user(random_username, "abc")
        assert result is None
