from django.db import models
from Backstore.models import ProductModel
from UserManagement.models import UserManageModel


class ShoppingCartModel(models.Model):

    anonymous_user_id = models.CharField(max_length=36, null=True, blank=True)
    user = models.OneToOneField(UserManageModel, related_name="shopping_cart", on_delete=models.CASCADE,
                                null=True, blank=True)

    products = models.ManyToManyField(ProductModel, through='CartItemModel')
    pay_tried = models.BooleanField(default=False)  # this is for creating an invoice.
    # maybe you wanted to add a field for next_cart

    def __str__(self):
        return f"shopping cart for {self.user.username}"


class CartItemModel(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCartModel, on_delete=models.CASCADE)
    products = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)




