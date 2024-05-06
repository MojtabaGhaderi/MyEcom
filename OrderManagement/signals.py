from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from OrderManagement.models import OrdersModel
from PayManagement.models import InvoiceModel


@receiver(post_save, sender=OrdersModel)
def order_post_save_handler(sender, instance, **kwargs):
    invoice = instance.order
    products = invoice.invoice_products.all()
    all_immediate_delivery = True
    for product in products:
        if not product.immediate_delivery:
            all_immediate_delivery = False
            break

    if all_immediate_delivery:
        pass  # deliver the products right now

    else:
        instance.status = "Progressing"



