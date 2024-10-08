# Generated by Django 5.0.7 on 2024-08-27 06:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0010_remove_package_tests_package_tests'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lab', models.ForeignKey(limit_choices_to={'is_lab': True}, on_delete=django.db.models.deletion.CASCADE, related_name='lab', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(limit_choices_to={'is_customer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='lab_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
