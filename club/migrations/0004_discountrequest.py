# Generated by Django 4.1.6 on 2023-05-06 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_clubbooking_clubbookingitem_cluborder_cluborderitem_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_request', to='club.account')),
            ],
        ),
    ]
