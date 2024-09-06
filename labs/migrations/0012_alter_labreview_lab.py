# Generated by Django 5.0.7 on 2024-08-29 03:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0011_labreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labreview',
            name='lab',
            field=models.ForeignKey(limit_choices_to={'is_lab': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]