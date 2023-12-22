import app_requests


def get_messages(token):
    url = "http://127.0.0.1:8000/message_history"  # replace with your server URL
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(response.text)
    data = response.json()

    if data["result"] == "error" and data["error"] == "No messages found":
        print("No messages found for this user.")
    else:
        print("Messages:", data["messages"])


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtcldoaXRlIiwiZXhwIjoxNzAzMDQ3MzY4fQ.QIrTMMGLJNNq3ccByyLPB1oktbrnXo0TWf5XvN2QV20"  # input("JWT Token: ")

get_messages(token)
