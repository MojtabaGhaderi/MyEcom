from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from OrderManagement.models import OrdersModel
from PayManagement.models import InvoiceModel, InvoiceItemModel
from SalesStatics.models import SalesModel


@receiver(post_save, sender=OrdersModel)
def order_post_save_handler(sender, instance, **kwargs):
    invoice = instance.invoice
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


@receiver(post_save, sender=OrdersModel)
def statics_data(sender, instance, **kwargs):
    if instance.status == 'Delivered':

        invoice = instance.invoice
        products = invoice.invoice_products.all()
        for product in products:
            static = SalesModel.objects.get_or_create(product=product)
            static.total_sold += product.quantity
            if product.discount:
                static.sold_in_discount += product.quantity
            if product.special_offer:
                static.sold_in_special_offer += product.quantity
            static.save()

