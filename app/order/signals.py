from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem


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
    if instance.order.is_paid:
        return
    product = instance.product
    product.qty_in_stock += instance.quantity
    product.save()


# A version that solves `n+1 query` problem
# @receiver(post_delete, sender=Order)
# def restore_product_quantity(sender, instance, **kwargs):
#     """
#     Restore the product quantity if not paid order is deleted/canceled
#     (with it's order items)
#     """
#     # Skip restoring if the order is paid
#     if instance.is_paid:
#         return
#     order_items = instance.order_items.all().select_related("product")
#     for order_item in order_items:
#         product = order_item.product
#         product.qty_in_stock += order_item.quantity
#         product.save()


@receiver(post_save, sender=Order)
def create_order_items(sender, instance, created, **kwargs):
    """Create order items for just created order"""
    if not created:
        return

    # cart_items = instance.user.cart.cart_items.all()
    # Modification to avoid n+1 query problem
    cart_items = instance.user.cart.cart_items.all().select_related("product")
    out_stock_errors = {}
    # Create order items based on cart items
    for item in cart_items:
        # Collect out of stock errors, if present
        if item.quantity > item.product.qty_in_stock:
            out_stock_errors[item.product.name] = (
                f"{item.quantity} > {item.product.qty_in_stock}"
            )
            continue

        instance.order_items.create(
            product=item.product,
            quantity=item.quantity,
        )

    if out_stock_errors:
        error = {
            "detail": "Quantity of ordered items exceeds product quantity in stock",
            "products": out_stock_errors,
        }
        instance.delete()
        # TODO: Make this return user friendly error msg in admin panel
        raise ValidationError(error)
