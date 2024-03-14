from django.db import models
from django.db.models.query import QuerySet


class PublishedLessonManager(models.Manager):
    """
    Менеджер.

    Возвращает опубликованные уроки.
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(
            is_published=True,
            category__is_published=True
        )
