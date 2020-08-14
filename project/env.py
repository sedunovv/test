import os


# celery
BROKER_URL = os.getenv('BROKER_URL', 'amqp://guest:guest@localhost:5672/')
