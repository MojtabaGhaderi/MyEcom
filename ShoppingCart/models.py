from django.db import models
from ProductCatalog.models import ProductModel
from UserManagement.models import UserManageModel


class ShoppingCartModel(models.Model):
    user = models.OneToOneField(UserManageModel, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel)
    product_number = models.ForeignKey(products, on_delete=models.CASCADE)

    # maybe you wanted to add a field for next_cart

    def __str__(self):
        return f"shopping cart for {self.user.username}"


class RecipeModel(models.Model):
    shopped = models.ForeignKey(ShoppingCartModel, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(UserManageModel, on_delete=models.DO_NOTHING)
    payed = models.BooleanField(default=False)


