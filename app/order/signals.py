from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from .models import Order, OrderItem


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Update order's total whenever an order item for it is
    created
    """
    order = instance.order
    total = sum(item.get_total_cost() for item in order.order_items.all())
    order.total = round(total, 2)
    order.save()
