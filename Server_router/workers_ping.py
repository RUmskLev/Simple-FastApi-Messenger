import requests


def loadup():
    url = "http://192.168.0.100:8000/loadup"
    response = requests.get(url)
    return response.text


# usage:
print(loadup())
