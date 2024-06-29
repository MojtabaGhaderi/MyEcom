# Generated by Django 5.0.6 on 2024-06-10 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCart', '0007_shoppingcartmodel_anonymous_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartmodel',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
    ]
