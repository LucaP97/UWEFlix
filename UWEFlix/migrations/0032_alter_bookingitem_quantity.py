# Generated by Django 4.1.6 on 2023-03-20 14:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0031_merge_20230320_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
