# Generated by Django 3.2.16 on 2024-03-05 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Тема теоретчиеского урока', max_length=250, verbose_name='Заголовок')),
                ('text', models.TextField(help_text='Текст теории', verbose_name='Текст теории')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('slug', models.SlugField(blank=True, help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', max_length=100, unique=True, verbose_name='Адрес для страницы с заметкой')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='lessons.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Теоретчиеский урок',
                'verbose_name_plural': 'Теоретические уроки',
                'ordering': ('pk',),
            },
        ),
    ]