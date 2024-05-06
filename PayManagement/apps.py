from django.apps import AppConfig


class PaymentgatewayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PayManagement'

    def ready(self):
        import PayManagement.signals