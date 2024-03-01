from django.apps import AppConfig


class UsermanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UserManagement'

    # def ready(self):
    #     import UserManagement.signals
