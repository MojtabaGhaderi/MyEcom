# Generated by Django 5.0 on 2024-02-18 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backstore', '0010_productmodel_date_added_productmodel_recently_added'),
        ('ShoppingCart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartmodel',
            name='products',
            field=models.ManyToManyField(through='ShoppingCart.CartItemModel', to='Backstore.productmodel'),
        ),
    ]
