from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, PaymentCreateView, PaymentAcceptView

app_name = "order"

router = DefaultRouter()
router.register("orders", OrderViewSet)


urlpatterns = [
    path(
        "orders/<int:order_pk>/create-payment/",
        PaymentCreateView.as_view(),
        name="pay",
    ),
    path("payment-webhook/", PaymentAcceptView.as_view(), name='payment-webhook'),
    path("", include(router.urls)),
]
