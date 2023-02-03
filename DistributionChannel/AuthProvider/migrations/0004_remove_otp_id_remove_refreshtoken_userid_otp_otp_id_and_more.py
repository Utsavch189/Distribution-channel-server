# Generated by Django 4.1.5 on 2023-02-03 14:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthProvider', '0003_alter_businessusers_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='id',
        ),
        migrations.RemoveField(
            model_name='refreshtoken',
            name='userid',
        ),
        migrations.AddField(
            model_name='otp',
            name='otp_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='refreshtoken',
            name='token_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='refreshtoken',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='AuthProvider.businessusers'),
        ),
        migrations.AlterField(
            model_name='businessusers',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 3, 14, 1, 50, 544689, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 3, 14, 1, 50, 545689, tzinfo=datetime.timezone.utc)),
        ),
    ]
