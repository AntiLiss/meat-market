from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authentication import authenticate
from user.models import ShippingAddress, Profile


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
        fields = [
            "user",
            "country",
            "city",
            "street",
            "house",
            "apartment",
            "postal_code",
            "latitude",
            "longtitude",
        ]
        read_only_fields = ["user"]


class ProfileSerializer(serializers.ModelSerializer):
    """Customer profile serializer"""

    class Meta:
        model = Profile
        fields = [
            "user",
            "first_name",
            "last_name",
            "telephone",
            "profile_photo",
        ]
        read_only_fields = ["user"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """User credentials serializer for register"""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password"]
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
        fields = UserRegisterSerializer.Meta.fields + ["profile", "shipping_address"]
