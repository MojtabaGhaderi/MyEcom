from django.db import models

from ShoppingCart.models import InvoiceModel
from UserManagement.models import UserManageModel


class PaymentModel(models.Model):
    # user = models.OneToOneField(UserManageModel, related_name="payment", on_delete=models.CASCADE)
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=15, decimal_places=3, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id}"

