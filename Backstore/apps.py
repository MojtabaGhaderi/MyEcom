# this app handles: adding products-editing them-creating new categories etc. this app is for admins only.

from django.apps import AppConfig


class ProductcatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Backstore'

    def ready(self):
        import Backstore.signals
