from django.db import models
from UserManagement.models import UserManageModel


# // purpose: storing categories and their relationship.//
class CategoryModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    parent = models.ManyToManyField('self', related_name='children', blank=True, null=True, symmetrical=False)

    def __str__(self):
        return self.name


# // purpose: storing data, about products.//
class ProductModel(models.Model):
    category = models.ManyToManyField(CategoryModel, symmetrical=False, related_name='category')

    name = models.CharField(unique=True, max_length=255, null=True)
    numbers = models.PositiveIntegerField(default=1)  # change this to quantity
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(null=True, blank=True, max_length=127)
    price = models.DecimalField(max_digits=13, decimal_places=3, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # this is percentage.
    available = models.BooleanField(default=True)
    sold_counts = models.IntegerField(default=0, editable=False)  # this only change throughout sold signal.
    likes = models.IntegerField(default=0, editable=False)  # this only change throughout signal.
    special_offer = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    recently_added = models.BooleanField(default=False)

    immediate_delivery = models.BooleanField(default=True)

    @property   # // a property which calculates final price of a product, based on original price and discount.//
    def final_price(self):
        discount_amount = self.price * (self.discount/100)
        return self.price - discount_amount


# // purpose: storing images of a product.//
class ProductImage(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='images/product_image', blank=True)  # check if you want to use caching


# // purpose: storing user's comments related to a product.//
class ProductComment(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(UserManageModel, on_delete=models.DO_NOTHING, related_name='user_comment')
    comment = models.CharField(max_length=512)


class NotificationModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/notifications', blank=True, null=True)

