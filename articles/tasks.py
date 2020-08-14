import asyncio
import json
import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from .models import Article
from .helpers import start_download, extract_data

logger = get_task_logger(__name__)


@shared_task(name='parse_articles')
def task_parse_articles(urls=None):
    if urls is None:
        file_path = f"{settings.MEDIA_ROOT}/data/urls.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                urls = file.read()
            urls = json.loads(urls)
        else:
            return "File with urls to parse didn't found"
    else:
        urls = urls.split(',')
        urls = list(filter(lambda x: x, urls))
    loop = asyncio.get_event_loop()
    parsed_data = loop.run_until_complete(start_download(urls))
    success_data = [x for x in parsed_data if isinstance(x, tuple)]
    failed_data = [x for x in parsed_data if not isinstance(x, tuple)]
    failed_data = [Article(url=x.url, status=2, err_message=str(x)) for x in failed_data]
    Article.objects.bulk_create(failed_data)
    success_data = extract_data(success_data)
    success_data = [Article(url=x['URL'], text=x['text'], status=1) for x in success_data]
    Article.objects.bulk_create(success_data)
    return "Task finished"
