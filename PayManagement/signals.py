from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from OrderManagement.models import OrdersModel
from PayManagement.models import InvoiceModel


@receiver(pre_save, sender=InvoiceModel)
def pre_save_handler(sender, instance, **kwargs):

    if instance.order:
        pass

    else:
        user = instance.user
        status = "Pending"

        order = OrdersModel(user=user, invoice=instance, status=status)
        order.save()

