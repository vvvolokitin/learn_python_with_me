# Generated by Django 3.2.16 on 2024-03-15 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_rename_wrong_result_balls'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=255, verbose_name='Уровень сложности')),
                ('scores', models.IntegerField(default=1, verbose_name='Баллы')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_level', to='lessons.testquestion', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Уровень сложности',
                'verbose_name_plural': 'Уровни сложности',
            },
        ),
    ]
