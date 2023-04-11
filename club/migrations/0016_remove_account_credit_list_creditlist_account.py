# Generated by Django 4.1.6 on 2023-04-11 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0015_creditlist_remove_statements_amount_due_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='credit_list',
        ),
        migrations.AddField(
            model_name='creditlist',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='credit_list', to='club.account'),
            preserve_default=False,
        ),
    ]
