# Generated by Django 4.1.5 on 2023-02-16 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('micro_brandCategoryProduct_service', '0007_alter_brand_created_at_and_more'),
        ('micro_auth_service', '0010_alter_businessusers_created_at'),
        ('micro_business_service', '0003_stock_imported_from_alter_stock_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPriceForWholesalerAndRetailer',
            fields=[
                ('price_id', models.CharField(default='', max_length=50, primary_key=True, serialize=False)),
                ('price', models.CharField(default='', max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='micro_brandCategoryProduct_service.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='micro_auth_service.businessusers')),
            ],
        ),
    ]
