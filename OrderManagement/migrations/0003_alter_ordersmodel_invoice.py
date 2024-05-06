# Generated by Django 5.0 on 2024-04-30 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0002_ordersmodel_delete_orders'),
        ('PayManagement', '0004_invoiceitemmodel_invoicemodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersmodel',
            name='invoice',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='order_invoice', to='PayManagement.invoicemodel'),
        ),
    ]
