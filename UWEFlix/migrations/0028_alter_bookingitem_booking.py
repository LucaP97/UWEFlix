# Generated by Django 4.1.6 on 2023-03-20 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0027_alter_bookingitem_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingitem',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='UWEFlix.booking'),
        ),
    ]
