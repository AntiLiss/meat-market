from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductDiscount


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""

    class Meta:
        model = Category
        fields = ("id", "name")


class ProductImageSerializer(serializers.ModelSerializer):
    """Product's image serializer"""

    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""

    # Images related to the product
    images = ProductImageSerializer(many=True)
    # Extra field with price after discount
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "description",
            "brand",
            "qty_in_stock",
            "properties",
            "rating",
            "price",
            "final_price",
            "discount",
            "images",
        )

    # Get price after discount using object's method
    # and set it for final_price field
    def get_final_price(self, obj):
        return obj.calculate_final_price()


class ProductDiscountSerializer(serializers.ModelSerializer):
    """Product discount serializer"""

    class Meta:
        model = ProductDiscount
        fields = (
            "id",
            "name",
            "description",
            "discount_percent",
            "start_date",
            "end_date",
            "is_active",
        )
