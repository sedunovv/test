#!/bin/sh

# wait for RabbitMQ server to start
sleep 5
celery -A project worker --beat --scheduler django --loglevel=info