# Generated by Django 4.1.5 on 2023-02-16 05:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_auth_service', '0006_rename_created_at_otp_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 16, 5, 17, 39, 656723, tzinfo=datetime.timezone.utc)),
        ),
    ]
