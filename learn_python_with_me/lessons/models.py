from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


from lessons.managers import PublishedLessonManager

User = get_user_model()


class Category(models.Model):
    """Модель 'Категории'."""

    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть категорию.'
    )

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель 'Теоретического урока'."""

    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок',
        help_text='Тема теоретчиеского урока'
    )
    text = RichTextField(
        verbose_name='Текст теории',
        help_text='Текст теории'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    slug = models.SlugField(
        'Адрес для страницы с заметкой',
        max_length=100,
        unique=True,
        blank=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='lessons'
    )

    objects = models.Manager()
    published_lessons = PublishedLessonManager()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Теоретчиеский урок'
        verbose_name_plural = 'Теоретические уроки'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            max_slug_length = self._meta.get_field('slug').max_length
            self.slug = slugify(self.title)[:max_slug_length]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'lessons:detail',
            kwargs={
                'category_slug': self.category.slug,
                'lesson_slug': self.slug,
            }
        )

    def get_test_url(self):
        return reverse(
            'lessons:test',
            kwargs={
                'category_slug': self.category.slug,
                'lesson_slug': self.slug,
                'question_id': self.lesson_questions.first().pk
            }
        )


class Comment(models.Model):
    """Модель'Комментария'."""
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите комментарий'
    )
    post = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый урок'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_by_author'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть комментарий.'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class LevelQuestion(models.Model):

    level_name = models.CharField(
        max_length=255,
        verbose_name='Уровень сложности'
    )
    scores = models.IntegerField(
        default=1,
        verbose_name='Баллы'
    )

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'

    def __str__(self) -> str:
        return self.level_name


class TestQuestion(models.Model):
    class QuestionType(models.TextChoices):
        single = 'single'
        multiple = 'multiple'

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_questions',
        verbose_name='Урок',
    )
    level = models.ForeignKey(
        LevelQuestion,
        on_delete=models.CASCADE,
        related_name='level_questions',
        verbose_name='Уровень сложности',
        default=1,
    )
    question = models.CharField(
        max_length=500,
        verbose_name='Вопрос'
    )

    question_type = models.CharField(
        max_length=8,
        choices=QuestionType.choices,
        default=QuestionType.single
    )

    def get_answer(self):
        if self.question_type == 'single':
            return self.answer_set.filter(
                is_correct=True
            ).first()
        else:
            qs = self.answer_set.filter(
                is_correct=True
            ).values()
            return [i.get('name') for i in qs]

    def user_can_answer(self, user):
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self)
        return not done.exists()

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['lesson__id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def get_answers(self):
        return self.question_answers.all()


class TestAnswer(models.Model):
    question = models.ForeignKey(
        TestQuestion,
        on_delete=models.CASCADE,
        related_name='question_answers',
        verbose_name='Вопрос'
    )
    answer = models.CharField(
        max_length=255
    )
    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Choice(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        TestQuestion,
        on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        TestAnswer,
        on_delete=models.CASCADE
    )


class Result(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_results'

    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='results'
    )
    correct = models.IntegerField(
        default=0
    )
    scores = models.IntegerField(
        default=0
    )
    test_complete = models.BooleanField(
        default=False
    )
