# Generated by Django 4.1.6 on 2023-03-31 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_club_club_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
