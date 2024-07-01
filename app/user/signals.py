from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from .models import Cart, CartItem


@receiver(post_save, sender=get_user_model)
def create_cart_for_user(sender, instance, created, **kwargs):
    """Create a cart for the new user"""
    if created:
        Cart.objects.create(user=instance)


@receiver([post_save, post_delete], sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    """
    Update cart's total whenever a cart item for it is
    created, updated or deleted
    """
    # TODO: Check whether an error occurs if i delete a cart itself or the user
    cart = instance.cart
    total = sum(item.get_total_cost() for item in cart.cart_items.all())
    cart.total = round(total, 2)
    cart.save()
