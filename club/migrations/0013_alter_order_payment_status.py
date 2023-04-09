# Generated by Django 4.1.6 on 2023-04-09 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0012_alter_order_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1),
        ),
    ]
