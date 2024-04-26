# Generated by Django 5.0 on 2024-03-02 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCart', '0003_alter_shoppingcartmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicemodel',
            name='amount',
            field=models.DecimalField(decimal_places=3, default=100, max_digits=15),
        ),
        migrations.AlterField(
            model_name='invoicemodel',
            name='invoice_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]