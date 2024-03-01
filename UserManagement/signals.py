# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.db.models.signals import post_save, pre_save
#
# import UserManagement
# from ShoppingCart.models import ShoppingCartModel
#
#
# @receiver(post_save, sender=UserManagement)
# def cart_create(sender, instance, created, **kwargs):
#     if created:
#         print("we are in signalssssssssssssssss")
#         shopping_cart = ShoppingCartModel.objects.create(user=instance)
#         print('done!!!!!!!!!')
#
