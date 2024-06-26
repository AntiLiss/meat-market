from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import authenticate
from .models import ShippingAddress, Profile, WishItem, Cart, CartItem


class AuthTokenSeralizer(serializers.Serializer):
    """Serializer for authentication token"""

    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        # Ensure the credentials match to user
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(username=email, password=password)

        # If there's no mathcing user return error
        if not user:
            raise serializers.ValidationError("Incorrect credentials!")

        # If the user exists add him to validated data
        attrs["user"] = user
        return attrs


class ShippingAddressSerializer(serializers.ModelSerializer):
    """Customers's shipping address serializer"""

    class Meta:
        model = ShippingAddress
        fields = (
            "user",
            "country",
            "city",
            "street",
            "house",
            "apartment",
            "postal_code",
            "latitude",
            "longtitude",
        )
        read_only_fields = ("user",)


class ProfileSerializer(serializers.ModelSerializer):
    """Customer profile serializer"""

    class Meta:
        model = Profile
        fields = (
            "user",
            "first_name",
            "last_name",
            "telephone",
            "profile_photo",
        )
        read_only_fields = ("user",)


class UserRegisterSerializer(serializers.ModelSerializer):
    """User credentials serializer for register"""

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserSerializer(UserRegisterSerializer):
    """Detailed user serializer"""

    profile = ProfileSerializer()
    shipping_address = ShippingAddressSerializer()

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + ("profile", "shipping_address")


class WishItemSerializer(serializers.ModelSerializer):
    """Wish item serializer"""

    class Meta:
        model = WishItem
        fields = ("id", "user", "product")
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        this_user = self.context.get("request").user
        product_id = self.validated_data.get("product")
        # Error if the user tries to wish the same product again
        if WishItem.objects.filter(user=this_user, product=product_id):
            error = "You have already wished this product!"
            raise ValidationError({"detail": error})

        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Cart serializer for reading"""

    class Meta:
        model = Cart
        fields = ("user", "total")


class CartItemSerializer(serializers.ModelSerializer):
    """Cart item serializer for CRD operations"""

    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity", "total_cost")
        read_only_fields = ("id", "cart")

    def get_total_cost(self, obj):
        return obj.get_total_cost()

    # Handle `unique_cart_product` constraint violation
    def create(self, validated_data):
        cart_id = validated_data.get("cart")
        product_id = validated_data.get("product")
        # Error if the user tries to add the same product to cart again
        if CartItem.objects.filter(cart=cart_id, product=product_id):
            error = "You have already added this item to your cart!"
            raise ValidationError({"detail": error})
        return super().create(validated_data)


class CartItemUpdateSerializer(CartItemSerializer):
    """Cart item serializer for update operations"""

    class Meta(CartItemSerializer.Meta):
        # Make `product` field unable to update
        read_only_fields = CartItemSerializer.Meta.read_only_fields + ("product",)
