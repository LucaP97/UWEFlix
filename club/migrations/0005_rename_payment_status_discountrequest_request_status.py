# Generated by Django 4.1.6 on 2023-05-06 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0004_discountrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountrequest',
            old_name='payment_status',
            new_name='request_status',
        ),
    ]
