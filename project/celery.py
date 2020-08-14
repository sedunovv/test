from __future__ import absolute_import, unicode_literals
from celery import Celery

from .env import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
os.environ.setdefault('C_FORCE_ROOT', 'true')

app = Celery('project', broker=BROKER_URL, backend=BROKER_URL, include=['articles.tasks'])
app.autodiscover_tasks()
