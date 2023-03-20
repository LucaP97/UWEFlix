# Generated by Django 4.1.6 on 2023-03-20 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UWEFlix', '0032_alter_customer_card_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemamanager',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cinema_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
