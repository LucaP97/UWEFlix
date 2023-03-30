# Generated by Django 4.1.6 on 2023-03-19 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0026_remove_bookingitem_total_price'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookingitem',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='bookingitem',
            name='ticket_type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='bookingitem',
            unique_together={('booking', 'ticket_type')},
        ),
        migrations.RemoveField(
            model_name='bookingitem',
            name='ticket',
        ),
    ]