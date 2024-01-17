from django.db import models


class CategoryModel(models.Model):
    category = models.CharField(unique=True, max_length=100)
    parent = models.CharField(null=True, max_length=100)
    child = models.CharField(null=True, max_length=100)


class ProductModel(models.Model):
    pass
