from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """User model manager"""

    def create_user(self, email, password=None, **fields):
        """Create and return user"""
        # Ensure email is provided
        if not email:
            raise ValueError("User must have an email!")

        user = self.model(
            email=self.normalize_email(email),
            **fields,
        )
        user.set_password(password)  # Set password separately with hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **fields):
        if not email:
            raise ValueError("User must have an email!")

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

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.email
