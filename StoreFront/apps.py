# this app handles what users see, like a list of products etc. //
from django.apps import AppConfig


class StorefrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'StoreFront'
