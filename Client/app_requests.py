import aiohttp
import asyncio

TOKEN = ""


async def get_token(username, password):
    global TOKEN
    url = "http://185.229.65.227:8000/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": username,
        "password": password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            data = await response.json()
            print(data)


async def register(username, hashed_password):
    url = f"http://185.229.65.227:8000/register?user_username={username}&user_hashed_password={hashed_password}"
    headers = {"accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as resp:
            print(await resp.text())

# Python 3.7+


async def get_updates(TOKEN):
    url = "http://185.229.65.227:8000/check_updates"  # replace with your server URL
    headers = {"Authorization": f"Bearer {TOKEN}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()
            print(text)
            data = await response.json()

            if data["result"] == "error" and data["error"] == "No messages found":
                print("No messages found for this user.")
            else:
                print("Messages:", data["messages"])

# Python 3.7+
# asyncio.run(get_token("lev", "lev"))
# asyncio.run(get_updates("TOKEN"))


async def loadup():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://185.229.65.227:8000/loadup') as resp:
            print(await resp.text())

# Python 3.7+
asyncio.run(register("lev", "lev"))
# asyncio.run(loadup())
