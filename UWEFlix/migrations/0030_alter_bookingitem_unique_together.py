# Generated by Django 4.1.6 on 2023-03-20 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0029_alter_bookingitem_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookingitem',
            unique_together={('booking', 'ticket_type')},
        ),
    ]
