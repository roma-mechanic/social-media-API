# Social-media-API

This repository contains a REST API built with Python Django and Django REST Framework. It allows users to create an account, log in, and perform CRUD (Create, Read, Update, Delete) operations on posts and comments.

## Installation
Python must be already installed.\
Clone this repository to your local machine\
[Social-media API can be downloaded from:](https://github.com/roma-mechanic/social-media-API.git)\
Or\
git clone https://github.com/roma-mechanic/social-media-API.git

### How to run with Docker:

Important ! Docker must be already installed

- Create and fill in the .env file with user data according to the .env_sample file.
- Run app
```bash
docker-compose up --build
```
- Create admin user.
```bash
python manage.py createsuperuser
```
- Create / get JWT-token and authorization.
- Use planetarium-service application.
- All endpoints in swagger documentation 127.0.0.1.8000/api/doc/swagger/

