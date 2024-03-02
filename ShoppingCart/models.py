from django.db import models
from django.utils import timezone

from ProductCatalog.models import ProductModel
from UserManagement.models import UserManageModel


class ShoppingCartModel(models.Model):
    user = models.OneToOneField(UserManageModel, related_name="shopping_cart", on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel, through='CartItemModel')
    pay_tried = models.BooleanField(default=False)  # this is for creating an invoice.
    # maybe you wanted to add a field for next_cart

    def __str__(self):
        return f"shopping cart for {self.user.username}"


class CartItemModel(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCartModel, on_delete=models.CASCADE)
    products = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class InvoiceModel(models.Model):
    user = models.OneToOneField(UserManageModel, on_delete=models.CASCADE)
    invoice_products = models.ManyToManyField(ProductModel, through='InvoiceItemModel')
    payment_status = models.BooleanField(default=False)  # maybe later change this to a choice field.
    # or even a Charfield.
    amount = models.DecimalField(max_digits=15, decimal_places=3)
    invoice_number = models.CharField(max_length=20, unique=True)
    tracking_code = models.PositiveIntegerField(null=True, blank=True)  # for now null and blank is True
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            current_year = timezone.now().year
            last_invoice = InvoiceModel.objects.filter(
                invoice_number__startswith=current_year).order_by('-invoice_nuber').first

            if last_invoice:
                last_invoice_number = int(last_invoice.invoice_number.split('-')[1])
                new_invoice_number = f"{current_year}-{last_invoice_number + 1:04d}"

            else:
                new_invoice_number = f"{current_year}-0001"
            self.invoice_number = new_invoice_number
        super().save(*args, **kwargs)


class InvoiceItemModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)




