# Generated by Django 4.1.6 on 2023-05-05 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0007_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='image_uri',
        ),
    ]
