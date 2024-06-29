from django.conf import settings
from django.db import models

from PayManagement.models import InvoiceModel
from UserManagement.models import UserManageModel


class OrdersModel(models.Model):
    user = models.ForeignKey(UserManageModel, null=True, blank=True, on_delete=models.SET_NULL)
    anonymous_user_id = models.CharField(max_length=36, null=True, blank=True)
    invoice = models.OneToOneField(InvoiceModel, related_name='order_invoice', on_delete=models.SET_NULL,null=True, editable=False)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Progressing', 'Progressing'),
        ('Delivered', 'Delivered'),
    ])



