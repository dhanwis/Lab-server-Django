# Generated by Django 5.0.6 on 2024-07-29 05:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0005_alter_reservation_lab_alter_timeslot_lab'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_file', models.FileField(upload_to='test-result/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_result', to='labs.test')),
                ('user', models.ForeignKey(limit_choices_to={'is_customer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='test_result', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
