# Generated by Django 5.0.6 on 2024-06-19 11:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCart', '0008_shoppingcartmodel_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcartmodel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
