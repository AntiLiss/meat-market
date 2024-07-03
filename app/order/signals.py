from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from .models import Order, OrderItem


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Update order's total whenever an order item for it is created
    """
    order = instance.order
    total = sum(item.get_total_cost() for item in order.order_items.all())
    order.total = round(total, 2)
    order.save()


@receiver(post_save, sender=OrderItem)
def reserve_product_quantity(sender, instance, created, **kwargs):
    """
    Reserve the product quantity for order item
    """
    if created:
        product = instance.product
        product.qty_in_stock -= instance.quantity
        product.save()


@receiver(post_delete, sender=OrderItem)
def restore_product_quantity(sender, instance, **kwargs):
    """
    Restore the product quantity if not paid order is deleted/canceled
    (with it's order items)
    """
    # Skip restoring if the order is paid
    # (Safety net in case of deletion via the admin panel)
    if instance.order.is_paid:
        return
    product = instance.product
    product.qty_in_stock += instance.quantity
    product.save()
