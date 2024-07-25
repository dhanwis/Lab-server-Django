# Generated by Django 5.0.6 on 2024-07-25 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0003_alter_package_lab_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='lab',
            field=models.ForeignKey(limit_choices_to={'is_lab': True}, on_delete=django.db.models.deletion.CASCADE, related_name='lab_docter', to=settings.AUTH_USER_MODEL),
        ),
    ]
