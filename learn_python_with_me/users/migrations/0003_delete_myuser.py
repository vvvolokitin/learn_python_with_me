# Generated by Django 3.2.16 on 2024-03-16 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_myuser_experience'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
