# FastApi based messenger ![Version Badge](https://img.shields.io/badge/Demo-0.1.0-informational?logo=&style=flat-square&logoColor=333333&color=666666&labelColor=999999)
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

### Server router


seems its coming soon... 