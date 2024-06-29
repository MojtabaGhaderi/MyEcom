from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from OrderManagement.models import OrdersModel
from PayManagement.models import InvoiceModel
from ShoppingCart.models import ShoppingCartModel, CartItemModel


@receiver(pre_save, sender=InvoiceModel)
def pre_save_handler(sender, instance, **kwargs):
    if instance.successful_payment:
        user = instance.user
        try:
            users_shopping_cart = ShoppingCartModel.objects.all().filter(user=user).first()
            OrdersModel.objects.create(user=user, invoice=instance, status='Pending')


        except:
            users_shopping_cart = ShoppingCartModel.objects.all().filter(anonymous_user_id=instance.anonymous_user_id).first()
            OrdersModel.objects.create(anonymous_user_id=instance.anonymous_user_id, invoice=instance, status='Pending')

        items = CartItemModel.objects.filter(shopping_cart=users_shopping_cart)
        for item in items:
            item.delete()




