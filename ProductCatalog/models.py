from django.db import models, connection
from django.db.models import Q


class CategoryModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    parent = models.ManyToManyField('self', related_name='children', blank=True, null=True, symmetrical=False)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    category = models.ManyToManyField(CategoryModel, symmetrical=False, related_name='category')

    name = models.CharField(unique=True, max_length=255, null=True)
    numbers = models.PositiveIntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(null=True, blank=True, max_length=127)
    price = models.DecimalField(max_digits=13, decimal_places=3, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # this is percentage.
    available = models.BooleanField(default=True)
    sold_counts = models.IntegerField(default=0, editable=False)  # this only change throughout sold signal.
    likes = models.IntegerField(default=0, editable=False)  # this only change throughout sold signal.
    special_offer = models.BooleanField(default=False)

    @property
    def final_price(self):
        discount_amount = self.price * (self.discount/100)
        return self.price - discount_amount


class ProductImage(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='images/product_image', blank=True)  # check if you want to use caching
