# Generated by Django 4.1.6 on 2023-05-01 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0004_alter_order_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='price_type',
            field=models.SmallIntegerField(default=0),
        ),
    ]
