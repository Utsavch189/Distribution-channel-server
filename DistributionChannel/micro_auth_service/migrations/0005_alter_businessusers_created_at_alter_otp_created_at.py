# Generated by Django 4.1.5 on 2023-02-10 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_auth_service', '0004_alter_businessusers_created_at_alter_otp_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 10, 13, 25, 23, 926257, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
