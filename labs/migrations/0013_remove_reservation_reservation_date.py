# Generated by Django 5.0.7 on 2024-08-30 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0012_alter_labreview_lab'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_date',
        ),
    ]
