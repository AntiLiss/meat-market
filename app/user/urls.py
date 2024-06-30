from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterUserView,
    ObtainTokenView,
    ProfileCRUDView,
    AddressCRUDView,
    CredentialsReadUpdateView,
    UserReadDeleteView,
    WhishItemListView,
    WishItemDetailView,
)

app_name = "user"


urlpatterns = [
    path(
        "me/wishitems/<int:pk>/", WishItemDetailView.as_view(), name="wishitem-detail"
    ),
    path("me/wishitems/", WhishItemListView.as_view(), name="wishitem-list"),
    path("me/shipping-address/", AddressCRUDView.as_view(), name="shipping-address"),
    path("me/profile/", ProfileCRUDView.as_view(), name="profile"),
    path(
        "me/credentials/",
        CredentialsReadUpdateView.as_view(),
        name="credentials",
    ),
    path("me/", UserReadDeleteView.as_view(), name="user-details"),
    path("token/", ObtainTokenView.as_view(), name="token"),
    path("register/", RegisterUserView.as_view(), name="register"),
]
