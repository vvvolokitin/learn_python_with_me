from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    experience = models.IntegerField(
        verbose_name='Заработанные баллы',
        default=0
    )
