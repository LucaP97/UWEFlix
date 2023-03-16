# Generated by Django 4.1.6 on 2023-03-16 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0031_remove_booking_booking_ref_alter_ticket_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_showing_ref',
        ),
        migrations.AddField(
            model_name='ticket',
            name='showing',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='UWEFlix.showing'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_price',
            field=models.CharField(choices=[('S', '10'), ('A', '15'), ('C', '5')], default='S', max_length=1),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(choices=[('S', 'Student'), ('A', 'Adult'), ('C', 'Child')], default='S', max_length=1),
        ),
    ]