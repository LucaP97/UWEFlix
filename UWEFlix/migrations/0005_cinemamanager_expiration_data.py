# Generated by Django 4.1.6 on 2023-05-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0004_alter_order_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinemamanager',
            name='expiration_data',
            field=models.DateField(blank=True, null=True),
        ),
    ]
