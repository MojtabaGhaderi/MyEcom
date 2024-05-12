from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from .models import ProductModel


# // each time a product is saved, this signal checks if the quantity of it 0 or not. if it was 0, then make that
# product unavailable.//
@receiver(pre_save, sender=ProductModel)
def product_availability(sender, instance, **kwargs):
    if instance.numbers == 0:
        instance.available = False
    elif instance.numbers > 0 and not instance.available:
        instance.available = True


# // each time a product is saved, this signal makes sure to update the date_added field and recently_added field if
# necessary. //
@receiver(pre_save, sender=ProductModel)
def recently_added_products(sender, instance, **kwargs):
    try:
        old_instance = ProductModel.objects.get(pk=instance.pk)
    except ProductModel.DoesNotExist:
        old_instance = None

    if old_instance:
        if old_instance.numbers == 0 and instance.numbers > 0:
            instance.recently_added = True
            instance.date_added = timezone.now()
    else:
        instance.recently_added = True




