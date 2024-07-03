from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

app_name = "order"

router = DefaultRouter()
router.register("orders", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
