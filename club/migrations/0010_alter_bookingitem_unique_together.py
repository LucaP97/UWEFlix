# Generated by Django 4.1.6 on 2023-04-09 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('club', '0009_rename_object_id_bookingitem_showing_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookingitem',
            unique_together={('booking', 'showing_type', 'showing_id')},
        ),
    ]
