# Generated by Django 4.1.5 on 2023-02-16 06:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_brandCategoryProduct_service', '0007_alter_brand_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 16, 6, 51, 48, 405161, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 16, 6, 51, 48, 406161, tzinfo=datetime.timezone.utc)),
        ),
    ]
