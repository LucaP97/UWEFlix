# Generated by Django 4.1.6 on 2023-04-17 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0002_statement_account_id_statement_account_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statement',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='order_type',
        ),
        migrations.CreateModel(
            name='UweflixStatementItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveIntegerField(blank=True, null=True)),
                ('order_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='contenttypes.contenttype')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uweflix_statement_items', to='accounts.statement')),
            ],
        ),
        migrations.CreateModel(
            name='ClubStatementItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.PositiveIntegerField(blank=True, null=True)),
                ('account_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='contenttypes.contenttype')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_statement_items', to='accounts.statement')),
            ],
        ),
    ]
