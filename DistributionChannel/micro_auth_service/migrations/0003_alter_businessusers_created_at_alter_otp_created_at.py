# Generated by Django 4.1.5 on 2023-02-08 07:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_auth_service', '0002_alter_businessusers_created_at_alter_otp_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 8, 7, 23, 44, 715760, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 8, 7, 23, 44, 716758, tzinfo=datetime.timezone.utc)),
        ),
    ]
