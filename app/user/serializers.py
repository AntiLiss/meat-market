from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authentication import authenticate
from user.models import Address, CustomerProfile


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

        # If the user exists add him to validated data of the serializer
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Create user with hashing password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update user with hashing password"""
        password = validated_data.pop("password", None)
        super().update(instance, validated_data)

        # Set password with hashing if it's provided and save the object
        if password:
            instance.set_password(password)
            instance.save()

        return instance


class AddressSerializer(serializers.ModelSerializer):
    """Customers's shipping address serializer"""

    class Meta:
        model = Address
        fields = ["country", "city", "street_address", "postal_code"]


# class CustomerRegisterSerializer(serializers.ModelSerializer):
#     """CustomerProfile serializer without address fields"""

#     user = UserSerializer()

#     class Meta:
#         model = CustomerProfile
#         fields = ["user", "phone"]

#     def create(self, validated_data):
#         """Create CustomerProfile with necessary fields"""
#         user_data = validated_data.pop("user", None)
#         address_data = validated_data.pop("address", None)

#         # Create first a User to whom the CustomerProfile will link
#         user = get_user_model().objects.create_user(**user_data)
#         # If address data provided link CustomerProfile to the address
#         if address_data:
#             # Create new address or get existing one
#             address, created = Address.objects.get_or_create(**address_data)

#         profile = CustomerProfile.objects.create(
#             user=user,
#             **validated_data,
#         )
#         return profile


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Customer serializer with additional fields"""

    user = UserSerializer()
    # Make it's possible to don't include `address` field
    address = AddressSerializer(required=False)

    class Meta:
        model = CustomerProfile
        fields = ["user", "phone", "address"]

    def create(self, validated_data):
        """Create CustomerProfile with necessary fields"""
        user_data = validated_data.pop("user", None)
        address_data = validated_data.pop("address", None)

        # Create first a User to whom the CustomerProfile will link
        user = get_user_model().objects.create_user(**user_data)

        profile = CustomerProfile.objects.create(
            user=user,
            **validated_data,
        )
        # If address data provided link CustomerProfile to the address
        if address_data:
            # Create new address or get existing one
            address, created = Address.objects.get_or_create(**address_data)
            profile.address = address
            profile.save()
        return profile
