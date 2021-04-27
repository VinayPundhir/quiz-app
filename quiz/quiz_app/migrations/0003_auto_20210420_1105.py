# Generated by Django 3.2 on 2021-04-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0002_auto_20210420_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_a',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_b',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_c',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_d',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AddField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(to='quiz_app.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='right_options',
            field=models.ManyToManyField(related_name='right_options', to='quiz_app.Option'),
        ),
        migrations.AddField(
            model_name='question',
            name='wrong_options',
            field=models.ManyToManyField(related_name='wrong_options', to='quiz_app.Option'),
        ),
    ]
