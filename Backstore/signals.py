from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from .models import ProductModel, DiscountCodeModel


# // each time a product is saved, this signal checks if the quantity of it 0 or not. if it was 0, then make that
# product unavailable.//
# this signal has been tested in class TestProductListView
@receiver(pre_save, sender=ProductModel)
def product_availability(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.available = False
        instance.price = None
    elif instance.quantity > 0 and not instance.available:

        instance.available = True


# // each time a product is saved, this signal makes sure to update the date_added field and recently_added field if
# necessary. //
# this signal has been tested in class TestProductListView
@receiver(pre_save, sender=ProductModel)
def recently_added_products(sender, instance, **kwargs):
    try:
        old_instance = ProductModel.objects.get(pk=instance.pk)
    except ProductModel.DoesNotExist:
        old_instance = None

    if old_instance:
        if old_instance.quantity == 0 and instance.quantity > 0:
            instance.recently_added = True
            instance.date_added = timezone.now()
    else:
        instance.recently_added = True


@receiver(post_save, sender=DiscountCodeModel)
def discount_availability(sender, instance, **kwargs):
    try:
        if instance.used >= instance.quantity:
            instance.available = False
            instance.save()
    except Exception as e:
        # logger.error(f"Error updating discount code availability: {e}")
        print(e)





