# Generated by Django 5.0.6 on 2024-06-24 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0006_ordersmodel_anonymous_user_id_ordersmodel_updated_at_and_more'),
        ('PayManagement', '0007_alter_invoicemodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersmodel',
            name='invoice',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_invoice', to='PayManagement.invoicemodel'),
        ),
    ]
