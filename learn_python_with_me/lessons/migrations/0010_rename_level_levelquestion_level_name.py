# Generated by Django 3.2.16 on 2024-03-15 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_levelquestion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='levelquestion',
            old_name='level',
            new_name='level_name',
        ),
    ]
