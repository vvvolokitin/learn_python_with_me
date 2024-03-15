from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class PublishedNewsManager(models.Manager):
    """
    Менеджер.

    Возвращает опубликованные новости.
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
        )
