# Generated by Django 4.1.6 on 2023-03-19 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0024_bookingitem_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingitem',
            old_name='price',
            new_name='total_price',
        ),
    ]