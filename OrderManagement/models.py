from django.conf import settings
from django.db import models

from PayManagement.models import InvoiceModel
from UserManagement.models import UserManageModel


class OrdersModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    invoice = models.OneToOneField(InvoiceModel, related_name='order_invoice', on_delete=models.PROTECT, editable=False)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Progressing', 'Progressing'),
        ('Delivered', 'Delivered'),
    ])



