# Generated by Django 4.1.5 on 2023-02-16 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_auth_service', '0008_alter_businessusers_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 16, 5, 20, 37, 422733, tzinfo=datetime.timezone.utc)),
        ),
    ]