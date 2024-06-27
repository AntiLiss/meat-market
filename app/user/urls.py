from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

app_name = "user"


urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("token/", views.ObtainTokenView.as_view(), name="token"),
    # path('profile/')
    path("me/", views.ProfileRUDView.as_view(), name="me"),
]
