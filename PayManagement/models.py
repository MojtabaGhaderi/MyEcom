from django.db import models

from Backstore.models import ProductModel
from UserManagement.models import UserManageModel
from django.utils import timezone


class InvoiceModel(models.Model):
    user = models.ForeignKey(UserManageModel, null=True, blank=True, on_delete=models.SET_NULL)
    anonymous_user_id = models.CharField(max_length=36, null=True, blank=True)
    invoice_products = models.ManyToManyField(ProductModel, through='InvoiceItemModel')
    successful_payment = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=3)
    invoice_number = models.CharField(max_length=20, unique=True)
    refid = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            current_year = timezone.now().year
            last_invoice = InvoiceModel.objects.filter(
                invoice_number__startswith=current_year).order_by('-invoice_number').first()

            if last_invoice:
                print("last invoice is:", last_invoice)
                last_invoice_number = int(last_invoice.invoice_number.split('-')[1])
                new_invoice_number = f"{current_year}-{last_invoice_number + 1:04d}"

            else:
                new_invoice_number = f"{current_year}-0001"
            self.invoice_number = new_invoice_number
        super().save(*args, **kwargs)


class InvoiceItemModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE, related_name='invoice_items')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"Purchase of {self.product.name} on Invoice #{self.invoice.invoice_number}"

