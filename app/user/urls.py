from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterUserView,
    ObtainTokenView,
    ProfileCRUDView,
    AddressCRUDView,
    CredentialsReadUpdateView,
    UserReadDeleteView,
)

app_name = "user"

router = DefaultRouter()
# router.register("cart", CartItemViewSet, basename="cartitem")
# router.register("whishlist", WishItemViewSet, basename="wishitem")


urlpatterns = [
    # path("", include(router.urls)),
    path("me/shipping-address/", AddressCRUDView.as_view(), name="shipping-address"),
    path("me/profile/", ProfileCRUDView.as_view(), name="profile"),
    path("me/credentials/", CredentialsReadUpdateView.as_view(), name="credentials"),
    path("me/", UserReadDeleteView.as_view(), name="user-details"),
    path("token/", ObtainTokenView.as_view(), name="token"),
    path("register/", RegisterUserView.as_view(), name="register"),
]
