import aiohttp
from config import SERVER_HOST, SERVER_PORT


WORKER_HOST = ""
WORKER_PORT = 0


async def get_token(username, password):
    """
    Receives JWT token using given credentials.
    Sends request to worker server, which address and port could be received by calling get_worker_address_async().
    After they are stored in WORKER_HOST and WORKER_PORT variables.

    :param username: user's username.
    :param password: user's password.
    :return: returns token on success, otherwise returns an empty line.
    """
    url = f"http://{WORKER_HOST}:{WORKER_PORT}/token"
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
            return data.get("access_token", "")


async def register(username, password):
    """
    Sends registration request to worker server with user's given credentials.

    :param username: username, given by user.
    :param password: password, given by user.
    :return: Returns {"result": "success"} on success, otherwise None.
    """
    url = f"http://{WORKER_HOST}:{WORKER_PORT}/register?user_username={username}&user_password={password}"
    headers = {"accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as resp:
            data = await resp.json()
            if data["result"] == "error":
                print(f"Error: {data['error']}")
                return None
            return data


async def get_updates(token, last_message_hash: str):
    """
    Sends request to check, if there is any updates for user.

    :param token: JWT token, can be obtained by calling get_token() function with user's password and username.
    :param last_message_hash: Hash, generated, from last message, user received.
    :return: Returns [] if there is no updates or list of messages if there are any updates or error if token is not valid or no messages found.
    """
    url = f"http://{WORKER_HOST}:{WORKER_PORT}/check_for_updates"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"last_message_hash": last_message_hash}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=body) as response:
            text = await response.text()
            data = await response.json()

            if data["result"] == "error":
                if data["error"] == "No messages found":
                    print("No messages found for this user.")
                elif data["error"] == "No updates":
                    print("No updates")
            else:
                print("Messages:", data["messages"])
                return data["messages"]


async def get_history(token):
    """
    Sends request to get all messages, sent or received by user.

    :param token: JWT token, can be obtained by calling get_token() function with user's password and username.
    :return: Returns list of messages on success, otherwise error message.
    """
    url = f"http://{WORKER_HOST}:{WORKER_PORT}/message_history"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            if data["result"] == "error":
                print(data["error"])
                return {"error": data["error"]}
            else:
                return data["messages"]


async def new_message(recipient_username: str, message_text: str, token: str):
    """
    Sends request to register new message from user.

    :param recipient_username: dialog name, user who you want to send message.
    :param message_text: text of the message.
    :param token: JWT token, can be obtained by calling get_token() function with user's password and username.
    :return: Returns {"result": "success"} on success of error message otherwise.
    """
    url = f"http://{WORKER_HOST}:{WORKER_PORT}/send_message"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message_text": message_text, "recipient_username": recipient_username}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status != 200:
                print(f"Failed to send message. Status code: {response.status}\n{response}")


async def get_worker_address_async():
    """
    Sends request to router server to get worker server's address and working port.
    Writes received address and port in WORKER_HOST and WORKER_PORT variables.

    :return: Returns None.
    """
    global WORKER_HOST, WORKER_PORT
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/get_worker_address"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["error"]:
                    print(f"Error: {data['error']}")
                else:
                    print(f"Address: {data['address']}, Port: {data['port']}")
                    WORKER_HOST, WORKER_PORT = data["address"], data["port"]
            else:
                print(f"Failed to get worker address. Status code: {response.status}")
