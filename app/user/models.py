import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def generate_user_image_path(instance, filename):
    """Generate user image path with unique uuid filename"""
    extension = os.path.splitext(filename)[1]
    filename = f"{uuid4()}{extension}"
    return os.path.join("uploads", "user", filename)


class UserManager(BaseUserManager):
    """User model manager"""

    def create_user(self, email, password=None, **fields):
        """Create and return user with customer permissions"""

        user = self.model(
            email=self.normalize_email(email),
            **fields,
        )
        user.set_password(password)  # Set password separately with hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **fields):
        """Create and return user with admin permissions"""
        superuser = self.model(
            email=self.normalize_email(email),
            **fields,
        )
        superuser.set_password(password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """User (admin/customer) model"""

    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=70, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.email


class AdminProfile(models.Model):
    """Admin profile for super user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=50, unique=True)


class CustomerProfile(models.Model):
    """Customer profile for regular user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=50, unique=True)
    profile_photo = models.ImageField(
        upload_to=generate_user_image_path, blank=True, null=True
    )
    address = models.ForeignKey(
        to="Address",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )


class Address(models.Model):
    """Customer's shipping address"""

    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street_address = models.CharField(
        max_length=150,
        help_text="The combination of the street name, house number and apartment",
    )
    postal_code = models.CharField(max_length=50)
