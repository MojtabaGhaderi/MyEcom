import uuid

from django.db import models
from django.db.models import F

from Backstore.models import ProductModel
from UserManagement.models import UserManageModel


class ShoppingCartModel(models.Model):
    anonymous_user_id = models.CharField(max_length=36, null=True, blank=True)
    user = models.OneToOneField(UserManageModel, related_name="shopping_cart", on_delete=models.CASCADE,
                                null=True, blank=True)

    products = models.ManyToManyField(ProductModel, through='CartItemModel')
    pay_tried = models.BooleanField(default=False)  # this is for creating an invoice.
    # maybe you wanted to add a field for next_cart

    @property
    def total_price(self):
        total_price = 0
        if self.products:
            for cart_item in self.cartitemmodel_set.all():
                total_price += cart_item.products.final_price * cart_item.quantity

        return total_price

    def __str__(self):
        return f"shopping cart for {self.user.username}"


class CartItemModel(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCartModel, on_delete=models.CASCADE)
    products = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
        else:
            existing_cart_item = CartItemModel.objects.filter(
                shopping_cart=self.shopping_cart,
                products=self.products
            ).first()

            if existing_cart_item:
                existing_cart_item.quantity = F('quantity') + self.quantity
                existing_cart_item.save()
            else:
                super().save(*args, **kwargs)



