# Generated by Django 4.1.6 on 2023-05-09 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0009_alter_clubordercancellationrequest_club_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_number',
            field=models.IntegerField(),
        ),
    ]
