from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse


class Grade(models.Model):
    grade = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Уровень'
    )

    def __str__(self):
        return self.grade

    class Meta():
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'


class TagQuestion(models.Model):
    tag = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.tag

    class Meta():
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Question(models.Model):

    question = models.CharField(
        max_length=255,
        verbose_name='Вопрос'
    )
    answer = RichTextField(
        blank=True,
        default=None,
        verbose_name='Ответ'

    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    grade = models.ManyToManyField(
        Grade,
        blank=True,
        default=None,
        related_name='grade_questions',
        verbose_name='Уровень'
    )
    tags = models.ManyToManyField(
        TagQuestion,
        blank=True,
        default=None,
        related_name='tag_questions',
        verbose_name='Тэги'
    )

    def __str__(self):
        return self.question

    class Meta():
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def get_absolute_url(self):
        return reverse(
            'employment:detail',
            kwargs={
                'pk': self.pk
            }
        )
