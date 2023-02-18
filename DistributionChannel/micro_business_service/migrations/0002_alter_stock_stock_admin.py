# Generated by Django 4.1.5 on 2023-02-16 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('micro_auth_service', '0008_alter_businessusers_created_at'),
        ('micro_business_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stock_admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_admin', to='micro_auth_service.businessusers'),
        ),
    ]
