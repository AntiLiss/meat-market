from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import OrderItem, Order
from product.models import Product


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer"""

    class Meta:
        model = Order
        fields = ("id", "user", "shipping_address", "total", "is_paid")
        read_only_fields = ("id", "user", "shipping_address", "total", "is_paid")

    def create(self, validated_data):
        user = self.context["request"].user
        order = Order.objects.create(
            user=user,
            shipping_address=user.shipping_address,
            total=user.cart.get_total_amount(),
        )

        quantity_exceed_errors = {}
        # Create order items based on cart items
        # TODO: Make this work in admin panel too! (maybe use signal?)
        for item in user.cart.cart_items.all():
            # Accumulate quantity exceed errors if they are
            if item.quantity > item.product.qty_in_stock:
                quantity_exceed_errors[item.product.name] = (
                    f"{item.quantity} > {item.product.qty_in_stock}"
                )
                continue

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )

        if quantity_exceed_errors:
            error = {
                "detail": "The quantity of ordered items exceeds product quantity in stock",
                "products": quantity_exceed_errors,
            }
            order.delete()
            raise ValidationError(error)

        return order


class YookassaPaymentRequestSerializer(serializers.Serializer):
    """Serializer for yookassa payment creation"""

    return_url = serializers.URLField()


class YookassaPaymentResponseSerializer(serializers.Serializer):
    """Serializer for confirmation url return"""

    confirmation_url = serializers.URLField()
