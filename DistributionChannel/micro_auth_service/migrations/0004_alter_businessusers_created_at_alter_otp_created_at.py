# Generated by Django 4.1.5 on 2023-02-08 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_auth_service', '0003_alter_businessusers_created_at_alter_otp_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 8, 7, 24, 1, 635370, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 8, 7, 24, 1, 636372, tzinfo=datetime.timezone.utc)),
        ),
    ]