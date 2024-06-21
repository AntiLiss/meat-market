from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authentication import authenticate


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
        fields = ["name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
        }

    def create(self, validated_data):
        """Create user with hashing password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update user with hashing password"""
        password = validated_data.pop("password", None)
        super().update(instance, validated_data)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
