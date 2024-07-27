# Generated by Django 5.0.6 on 2024-07-24 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermanage',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
