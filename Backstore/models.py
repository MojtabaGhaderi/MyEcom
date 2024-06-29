from django.conf import settings
from django.db import models
from django.utils.text import slugify

from UserManagement.models import UserManageModel, AdminModel


# // purpose: storing categories and their relationship.//
class CategoryModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    parent = models.ManyToManyField('self', related_name='children', blank=True, symmetrical=False)

    def __str__(self):
        return self.name


# // purpose: adding tags to products. //
class TagsModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# // purpose: storing data, about products.//
class ProductModel(models.Model):
    category = models.ManyToManyField(CategoryModel, symmetrical=False, related_name='category')

    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(TagsModel, related_name='products', blank=True)
    price = models.DecimalField(max_digits=13, decimal_places=3, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # this is percentage.
    available = models.BooleanField(default=True)
    sold_counts = models.IntegerField(default=0, editable=False)  # this only change throughout sold signal.
    likes = models.IntegerField(default=0, editable=False)  # this only change throughout signal.
    special_offer = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    recently_added = models.BooleanField(default=False)

    immediate_delivery = models.BooleanField(default=True)

    @property   # // a property which calculates final price of a product, based on original price and discount.//
    def final_price(self):
        if self.price:
            discount_amount = self.price * (self.discount/100)
            return self.price - discount_amount
        else:
            return None

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# // purpose: storing images of a product.//
class ProductImage(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='images/product_image', blank=True)  # check if you want to use caching


# // purpose: storing user's comments related to a product.//
class ProductComment(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(UserManageModel, on_delete=models.SET_NULL, related_name='user_comment', null=True)
    comment = models.CharField(max_length=512)
    date_added = models.DateTimeField(auto_now=True)


# // purpose: storing Discount codes.//
class DiscountCodeModel(models.Model):
    discount_code = models.CharField(max_length=32, blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # percentage of the code.
    quantity = models.IntegerField(default=1)  # how many times the code can be used.
    time_period = models.DurationField(blank=True, null=True)  # for what period of time the code is available
    # who created this code:
    created_by = models.ForeignKey(UserManageModel, on_delete=models.CASCADE, null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    used = models.IntegerField(default=0)

    available = models.BooleanField(default=True)


# // purpose: storing news and notifications.//
class NotificationModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/notifications', blank=True, null=True)

