from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email="test@example.com", password=None, **fields):
    """Create user in db and return it"""
    return get_user_model().objects.create_user(email, password, **fields)


class UserModelTests(TestCase):
    """Test User model"""

    def test_create_user_with_email(self):
        """Test creating a user with email"""
        email = "test@example.com"
        password = "testpass"
        user = create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_creating_user_without_email_error(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            create_user(email="")

    def test_normalize_new_user_email(self):
        """Test whether new user's email is normalized"""
        sample_emails = [
            ["TEST@EXAMPLE.COM", "TEST@example.com"],
            ["Test@Example.com", "Test@example.com"],
            ["tesT@example.Com", "tesT@example.com"],
        ]

        for raw, expected in sample_emails:
            user = create_user(email=raw)
            self.assertEqual(user.email, expected)
