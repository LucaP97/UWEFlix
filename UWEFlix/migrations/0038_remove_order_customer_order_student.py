# Generated by Django 4.1.6 on 2023-03-30 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0037_remove_customer_birth_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='UWEFlix.student'),
            preserve_default=False,
        ),
    ]
