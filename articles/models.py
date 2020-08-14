from django.db import models
from .helpers import *


class Article(models.Model):
    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    url = models.CharField(verbose_name="Ссылка на статью", max_length=1500)
    text = models.TextField(verbose_name="Текст статьи", null=True, blank=True)
    status = models.SmallIntegerField(choices=((SUCCESS, 'SUCCESS'), (FAILED, 'FAILED')),
                                      verbose_name="Статус")
    err_message = models.CharField(verbose_name="Сообщение об ошибке", max_length=300, null=True, blank=True)
