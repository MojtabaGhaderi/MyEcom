from django.db import models

from Backstore.models import ProductModel


class SalesModel(models.Model):
    product = models.OneToOneField(ProductModel, related_name="sale-statics", on_delete=models.PROTECT)
    sold_in_discount = models.PositiveBigIntegerField(default=0)
    sold_in_special_offer = models.PositiveBigIntegerField(default=0)
    sold_in_discount_code = models.PositiveBigIntegerField(default=0)
    total_sold = models.PositiveBigIntegerField(default=0)


