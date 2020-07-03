from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Cart


@receiver(post_save, sender='shop.User', dispatch_uid='user_create')
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
