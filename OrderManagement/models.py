from django.conf import settings
from django.db import models

from UserManagement.models import UserManageModel


class Orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'pending'),
        ('preparing', 'preparing'),
        ('delivered', 'delivered'),
        ('canceled', 'canceled'),
    ])



