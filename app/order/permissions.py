from rest_framework.permissions import BasePermission


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
