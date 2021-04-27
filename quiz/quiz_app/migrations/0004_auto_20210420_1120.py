# Generated by Django 3.2 on 2021-04-20 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0003_auto_20210420_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='right_options',
        ),
        migrations.RemoveField(
            model_name='question',
            name='wrong_options',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='questions',
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quiz_app.question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='valid',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]
