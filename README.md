# ParseArticles

To run the project do the following
-
**1. build images**

docker-compose build

**2.a launching containers**

docker-compose up django rabbitmq celery

**2.b launching containers in the background**

docker-compose up -d django rabbitmq celery

**3. To apply migrations and create super user**

- docker-compose exec django bash
- ./manage.py migrate
- ./manage.py createsuperuser
