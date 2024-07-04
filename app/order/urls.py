from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, PaymentView

app_name = "order"

router = DefaultRouter()
router.register("orders", OrderViewSet)


urlpatterns = [
    path(
        "orders/<int:order_pk>/pay/",
        PaymentView.as_view(),
        name="pay",
    ),
    path("", include(router.urls)),
]
