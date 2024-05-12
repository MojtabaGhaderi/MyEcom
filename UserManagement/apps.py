# this app handles user related activities.

from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UserManagement'

    # def ready(self):
    #     import UserManagement.signals
