from django.db import models
from django.contrib.auth.models import AbstractUser
from ShoppingCart.models import ShoppingCartModel


class UserManageModel(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=11)

    def __str__(self):
        return self.username


