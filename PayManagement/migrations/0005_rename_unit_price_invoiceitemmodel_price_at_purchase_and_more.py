# Generated by Django 5.0.6 on 2024-06-21 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PayManagement', '0004_invoiceitemmodel_invoicemodel_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceitemmodel',
            old_name='unit_price',
            new_name='price_at_purchase',
        ),
        migrations.RenameField(
            model_name='invoicemodel',
            old_name='payment_status',
            new_name='successful_payment',
        ),
        migrations.AlterField(
            model_name='invoiceitemmodel',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='PayManagement.invoicemodel'),
        ),
    ]
