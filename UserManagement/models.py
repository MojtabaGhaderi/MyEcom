from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManageModel(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=11)

    def __str__(self):
        return self.username


class AdminModel(models.Model):
    user = models.OneToOneField(UserManageModel, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('super_admin', 'Super Admin'),
        ('regular_admin', 'Admin'),
    ])
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role}"
