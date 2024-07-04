from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import Order


class DoesUserHaveAddress(BasePermission):
    """Allow access only to user with shipping address"""

    message = "User must have an address to make orders!"

    def has_permission(self, request, view):
        shipping_address = getattr(request.user, "shipping_address", None)
        if not shipping_address:
            return False
        return True


class IsCartNotEmpty(BasePermission):
    """Allow access only to user with items in cart"""

    message = "Your cart is empty!"

    def has_permission(self, request, view):
        if not request.user.cart.cart_items.all():
            return False
        return True


class IsOrderNotPaid(BasePermission):
    """Allow acces only if the order is not paid"""

    message = "This order is already paid!"

    def has_permission(self, request, view):
        order_id = view.kwargs.get("order_pk")
        order = get_object_or_404(Order, pk=order_id)
        if order.is_paid:
            return False
        return True
