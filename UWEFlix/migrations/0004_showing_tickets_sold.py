# Generated by Django 4.1.6 on 2023-03-07 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0003_cinemamanager_film_screen_showing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='showing',
            name='tickets_sold',
            field=models.SmallIntegerField(default=0),
        ),
    ]
