# Generated by Django 5.0.6 on 2024-06-20 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCart', '0012_alter_shoppingcartmodel_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcartmodel',
            name='total_price',
        ),
    ]
