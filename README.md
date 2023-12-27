# FastApi based messenger ![Version Badge](https://img.shields.io/badge/Version-0.1.0-informational?logo=&style=flat-square&logoColor=333333&color=666666&labelColor=999999)
![MIT licence badge](https://img.shields.io/badge/License-MIT-blue.svg)

## Simple fully asynchronous messenger that uses FastApi + PostgreSQL and has graphical client

### Uses:
![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=plastic)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=plastic)
![PostgreSQL Badge](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=fff&style=plastic)
![SQLAlchemy Badge](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=plastic)

### Tested on:
![Debian 11 Badge](https://img.shields.io/badge/Debian-11-informational?logo=debian&style=flat&logoColor=be5666&color=ffffff&labelColor=a81d33)
![Debian 12 Badge](https://img.shields.io/badge/Debian-12-informational?logo=debian&style=flat&logoColor=be5666&color=ffffff&labelColor=a81d33)

This is system of servers, that work together and do specific tasks:

- Router server. Handles first connections and and chooses which worker server to redirect the user to, based on the workload of the worker servers.
- Worker server. Works with user and proceeds all operations. Works with database. They can be horizontal expanded infinitely.


## Installation

It's been tested on debian 11 and debian 12. Follow instructions to install needed server code on every machine:

Firstly, update apt packages:

```shell
sudo apt update && sudo apt upgrade -y
```

Then check if you have python 3.11.x and pip3 installed:

```shell
python3 --version
pip3 --version
```

If you haven't them on your machine, you can install them using following command:

```shell
sudo apt install python3 -y && sudo apt install python3-pip -y
```

Then clone git repository with code:

```shell
git clone https://github.com/RUmskLev/HSE-project-python-1-2-grade.git
```

Enter the directory, create a virtual environment here and activate it:

```shell
cd HSE-project-python-1-2-grade
python3 -m venv AppVenv
source venv/bin/activate
```

Then install all dependencies:

```shell
pip install -r requirements.txt
```

Now chose which app you would like to run and change .env file for it. You can see an example in .env.example:

***

### Server router

Edit .env file for server router:

```shell
nano Server_router/.env
```

You need to get something like this, but with your values. Use localhost for tests:

```dotenv
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

Then you can run the server using following command:

```shell
python3 Server_router/run.py
```

You will see some uvicorn logs and message, that server is running on ...

***

### Server worker

Edit .env file for server router:

```shell
nano Server_router/.env
```

You need to get something like this, but with your values. Use localhost for tests:

```dotenv
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
JWT_SECRET_KEY=1hjgh1ug1jg1ikhu1o1hl1ih1ohg8712841g29i4187y249184y194yu19gh49184y
HASHING_ALGORYTHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

DATABASE_HOST=localhost
DATABASE_NAME=Messenger
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_PORT=5432
```

Make sure you have installed postgresql server, and it works for outbound connections.

Create a database for messenger in psql shell or where you prefer more:

```postgresql
CREATE DATABASE Messenger;
```

Now you need to upgrade your database to last version, using alembic. run the following in your terminal:

```shell
alembic revision --autogenerate -m "Initial database creation"
```

It will generate you a migration file in migrations/versions folder, it will look like this:

```python
"""Initial database

Revision ID: dd12f10acbd9
Revises: 
Create Date: 2023-12-18 06:23:28.762443

"""
...
```

You will need Revision ID hash to upgrade your database to created migration. Run the following:

```shell
alembic upgrade [Revision ID]
```

Check that all tables created successfully.

Now you can run the server using following command:

```shell
python3 Server_worker/run.py
```

You will see some uvicorn logs and message, that server is running on ...

***

### Messenger client

Edit .env file for server router:

```shell
nano Client/.env
```

You need to get something like this, but with your values. Use localhost for tests:

```dotenv
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

where SERVER_HOST and SERVER_PORT are host and port for router server.

Then you can run the server using following command:

```shell
python3 Client/App.py
```

***

## You can always create an issue. this will help me make this project stable.
