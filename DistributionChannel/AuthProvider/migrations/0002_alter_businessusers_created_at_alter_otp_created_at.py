# Generated by Django 4.1.5 on 2023-02-03 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthProvider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 3, 8, 50, 42, 413803, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 3, 8, 50, 42, 414801, tzinfo=datetime.timezone.utc)),
        ),
    ]
