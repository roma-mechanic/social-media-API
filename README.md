# Social-media-API

This repository contains a REST API built with Python Django and Django REST Framework.
It allows users to create an account, log in, and perform CRUD (Create, Read, Update, Delete) operations on posts and
comments.

Additionally, it is possible to postpone the publication of a post for a specified time or publish at the right time
through the admin panel using selery-beat

## Installation

Python must be already installed.\
Clone this repository to your local machine\
[Social-media API can be downloaded from:](https://github.com/roma-mechanic/social-media-API/tree/develop)\
Or\
git clone https://github.com/roma-mechanic/social-media-API/tree/develop

### How to run with Docker:

Important ! Docker must be already installed

- Create and fill in the .env file with user data according to the .env_sample file.
- Run app

```bash
docker-compose up --build
```

- Create admin user.

```bash
docker exec -it <container ID> python manage.py createsuperuser
```

- Create / get JWT-token and authorization.
- Create schedule for running tasks posts published
- Create your User Profile
- Use planetarium-service application.
- All endpoints in swagger documentation 127.0.0.1.8000/api/doc/swagger/

## Project scheme
![Project scheme](media/uploads/demo/social_media_api_scheme.drawio.jpg)

## Demo swagger scheme endpoints
![swagger demo](media/uploads/demo/swagger_of_social_media_api.jpg)