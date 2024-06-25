from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from .serializers import AuthTokenSeralizer
from user.serializers import UserSerializer, CustomerProfileSerializer


class RegisterUserView(CreateAPIView):
    """Manage user creation"""

    serializer_class = CustomerProfileSerializer


class ObtainTokenView(ObtainAuthToken):
    """Manage auth token creation and obtaining"""

    serializer_class = AuthTokenSeralizer


class ProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Manage user profile retrieve, update, destroy operations"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
