# // this app handles the features for a shopping cart like adding product, changing in cart, emptying etc. //


from django.apps import AppConfig


class ShoppingcartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ShoppingCart'

    def ready(self):
        import ShoppingCart.signals
