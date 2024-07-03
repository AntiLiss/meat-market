from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import OrderItem, Order
from product.models import Product


# class OrderItemSerializer(serializers.ModelSerializer):
#     """Order item serializer"""

#     total_cost = serializers.SerializerMethodField()
#     # Get Product object from foreign key field `product`
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     class Meta:
#         model = OrderItem
#         fields = ("id", "order", "product", "quantity", "total_cost")
#         read_only_fields = ("id", "order")

#     def get_total_cost(self, obj):
#         return obj.get_total_cost()

#     # Ensure order_item's quantity doesn't exceed product's stock
#     def validate(self, attrs):
#         quantity = attrs.get("quantity")
#         product = attrs.get("product")
#         if quantity > product.qty_in_stock:
#             error = f"You can not buy more than we have! ({quantity} > {product.qty_in_stock})"
#             raise ValidationError(error)
#         return attrs


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
        )

        quantity_exceed_errors = {}
        # Create order items based on cart items
        # TODO: Maybe implement this via signal?
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
                "detail": "Order item quantity out of stock",
                "products": quantity_exceed_errors,
            }
            order.delete()
            raise ValidationError(error)

        return order
