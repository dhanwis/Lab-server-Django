# Generated by Django 5.0.7 on 2024-08-05 06:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0008_alter_testreviewreply_lab_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='lab',
            field=models.ForeignKey(default=5, limit_choices_to={'is_lab': True}, on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
