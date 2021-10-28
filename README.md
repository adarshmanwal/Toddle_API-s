# Toddle Backend Task (Virtual Classroom)

Simple stateless microservice with following API endpoints:
- Authentication endpoint
- REST API endpoints for a Virtual Classroom app (details below)

## Technologies used

- Python
- Django
- Django Rest framework
- Python JWT library (PyJWT)
- Postgres
- Heroku

## App live URL

App is deployed in Heroku URL is

https://toddleapi.herokuapp.com/

## API Postman collection

This is the link of postman collection:

https://www.getpostman.com/collections/0a4f74f9fb7768ae9b2e

Github link: https://github.com/adarshmanwal/Toddle_API-s/blob/master/postman_collection.json

## ER Diagram link

https://github.com/adarshmanwal/Toddle_API-s/blob/master/myapp_models.png

## How to run

Run migrations

```
python3 manage.py migrate
```

Run server

```
python3 manage.py runserver
```


## API end points

End Point | Method | Description | Post Data
--- | --- | --- | ---
/auth/tutor/login | POST | Login tutor api | username, password
/auth/student/login | POST | Login student api | username, password
/auth/tutor/profile | GET | Get Tutor profile | N/A
/auth/student/profile | GET | Get student profile | N/A
/auth/assignment | POST | Create assignment | description, dead_line_date, published_at
/auth/assignment | GET | Get all assignments | N/A
/auth/assignment?published_at=ongoing | GET | Get all ongoing assignments | N/A
/auth/assignment?status=pending | GET | Get pending assignments | N/A
/auth/assignment/delete/<id> | DELETE | Delete assignment | N/A
/auth/assignment/update/<id> | PUT | Update assignment | description, dead_line_date, published_at
/auth/assignment/submit/<id> | POST | Submit assignment | remark


## Authentication

We have two login API to generate access token:

- Tutor Login: /auth/tutor/login
- Student login: /auth/status/login

Note: Both API accepts any username and password for now and generates access token.

## Authentication header

All other APIs other then login API requires authentication header. Example:

```
Authorization: Barrer <access token>
```

## Future scope

- Login end point with correct details
- Register API for tutor and student
- Better API documentation