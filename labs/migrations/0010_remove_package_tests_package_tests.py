# Generated by Django 5.0.7 on 2024-08-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0009_test_lab'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='tests',
        ),
        migrations.AddField(
            model_name='package',
            name='tests',
            field=models.ManyToManyField(related_name='packages', to='labs.test'),
        ),
    ]
