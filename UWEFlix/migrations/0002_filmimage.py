# Generated by Django 4.1.6 on 2023-04-18 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='UWEFlix.film')),
            ],
        ),
    ]
