# Generated by Django 4.1.6 on 2023-03-08 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0007_alter_showing_film'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showing',
            name='screen',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='screen', to='UWEFlix.screen'),
        ),
    ]
