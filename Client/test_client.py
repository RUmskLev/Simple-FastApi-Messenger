import App
import app_requests
import config

config.SERVER_HOST = "5.182.86.173"
config.SERVER_PORT = 8000

app_requests.WORKER_HOST = "185.229.65.227"
app_requests.WORKER_PORT = 8000

App.app = App.MyApp()


def test_sync_log():
    user_login = "user"
    password = "password"
    user_step = "logged"
    App.sync_log(user_login, password, user_step)
    assert App.USER_STEP == user_step
    assert App.PASSWORD == password
    assert App.USERNAME == user_login
