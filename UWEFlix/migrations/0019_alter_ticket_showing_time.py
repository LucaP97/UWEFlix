# Generated by Django 4.1.6 on 2023-03-13 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0018_alter_booking_showing_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='showing_time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
