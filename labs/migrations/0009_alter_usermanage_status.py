# Generated by Django 4.2.7 on 2024-06-13 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0008_alter_usermanage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermanage',
            name='status',
            field=models.CharField(default='enable', max_length=20),
        ),
    ]