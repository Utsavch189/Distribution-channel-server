# Generated by Django 4.1.5 on 2023-02-16 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micro_business_service', '0005_rename_productpriceforwholesalerandretailer_setproductpriceforwholesalerandretailer'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='total_price',
            field=models.CharField(default='', max_length=20),
        ),
    ]
