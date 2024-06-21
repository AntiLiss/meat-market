from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

app_name = "user"

# router = DefaultRouter()
# router.register("users", UserListRetrieveViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("token/", views.ObtainTokenView.as_view(), name="token"),
    path("me/", views.ProfileRUDView.as_view(), name="me"),
]
