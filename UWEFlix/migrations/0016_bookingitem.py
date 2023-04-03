# Generated by Django 4.1.6 on 2023-03-17 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0015_alter_booking_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='UWEFlix.booking')),
                ('showing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UWEFlix.showing')),
            ],
            options={
                'unique_together': {('booking', 'showing')},
            },
        ),
    ]
