from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from PayManagement.models import InvoiceModel, InvoiceItemModel
from ShoppingCart.models import ShoppingCartModel


@receiver(post_save, sender=ShoppingCartModel)
def shopping_cart_pay_status(sender, instance, **kwargs):

    if instance.pay_tried:
        print("pay tried is:", instance.pay_tried)
        if instance.user:
            user = instance.user
            invoice = InvoiceModel.objects.create(user=user, amount=instance.total_price)
        else:
            invoice = InvoiceModel.objects.create(anonymous_user_id=instance.anonymous_user_id, amount=instance.total_price)

        print('this is cart items:', instance.products.all())

        for cart_item in instance.cartitemmodel_set.all():
            InvoiceItemModel.objects.create(
                invoice=invoice,
                product=cart_item.products,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.products.final_price
            )
