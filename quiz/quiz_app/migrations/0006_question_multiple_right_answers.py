# Generated by Django 3.2 on 2021-04-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0005_question_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='multiple_right_answers',
            field=models.BooleanField(default=False),
        ),
    ]