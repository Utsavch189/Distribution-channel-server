# Generated by Django 4.1.5 on 2023-02-11 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('micro_brandCategoryProduct_service', '0004_alter_brand_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('production_id', models.CharField(default='', max_length=50, primary_key=True, serialize=False)),
                ('product_number', models.CharField(default='', max_length=20)),
                ('production_date', models.CharField(default='', max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='micro_brandCategoryProduct_service.product')),
            ],
        ),
    ]