from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

from .managers import PublishedNewsManager
User = get_user_model()


class ProjectNews(models.Model):
    """Модель 'Публикации'."""
    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок'
    )
    text = RichTextField(
        verbose_name='Текст новости проекта'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    objects = models.Manager()
    published_news = PublishedNewsManager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class CommentOnProjectNews(models.Model):
    """Модель'Комментария'."""
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите комментарий'
    )

    project_news = models.ForeignKey(
        ProjectNews,
        on_delete=models.CASCADE,
        related_name='projects_news_comments',
        verbose_name='Комментируемая новость'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects_news_comments_by_author'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть комментарий.'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = ("Комментарий")
        verbose_name_plural = ("Комментарии")
