# Generated by Django 3.2 on 2021-04-25 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0010_auto_20210425_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='user_selected_option',
            field=models.TextField(default=None),
        ),
    ]
