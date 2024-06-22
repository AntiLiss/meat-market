from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from user.serializers import UserSerializer
from user.tests.test_models import create_user


PROFILE_URL = reverse("user:me")


class PublicUserProfileAPITests(TestCase):
    """Test unauthorized profile api requests"""

    def test_retrieve_profile_unauthorized(self):
        """Test unauthorized request returns error"""
        unauth_client = APIClient()
        res = unauth_client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserProfileAPITests(TestCase):
    """Test authenticated user profile api requiests"""

    # Set test environment
    def setUp(self):
        self.user = create_user(email="test@example.com", name="test")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_post_not_allowed(self):
        """Test POST method not allowed"""
        res = self.client.post(PROFILE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_profile(self):
        """Test retrieving user profile"""
        res = self.client.get(PROFILE_URL)
        profile_serializer = UserSerializer(self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Ensure profile data returned and they're correct
        self.assertEqual(res.data, profile_serializer.data)

    def test_partial_update_profile(self):
        """Test partial (patch) update of user profile"""
        original_name = self.user.name
        payload = {"email": "newemail@example.com"}
        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        # Ensure not listed field (name) remains untouched
        self.assertEqual(self.user.name, original_name)
        # Ensure user data returned in reponse
        user_serializer = UserSerializer(self.user)
        self.assertEqual(res.data, user_serializer.data)

    def test_full_update_profile_error(self):
        """Test full (put) update of user profile"""
        # NOTE: PUT method can omit fields that are blank=True
        payload = {"email": "newemail@example.com", "password": "newpass"}
        res = self.client.put(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
        # Ensure user data returned in reponse
        user_serializer = UserSerializer(self.user)
        self.assertEqual(res.data, user_serializer.data)

    def test_put_update_requires_all_fields(self):
        """Test put update returns error if not all fields provided"""
        payload = {"email": "newemail@mail.ru"}
        res = self.client.put(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure there is no update
        self.assertNotEqual(self.user.email, payload["email"])

    def test_delete_user(self):
        """Test deletion of user"""
        res = self.client.delete(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure the user no more exists in DB
        user_exists = get_user_model().objects.filter(id=self.user.id).exists()
        self.assertFalse(user_exists)
