import uuid
from yookassa import Configuration, Payment
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Order, Payment
from .serializers import OrderSerializer
from .permissions import DoesUserHaveAddress, IsCartNotEmpty, IsOrderNotPaid


class OrderViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """Manage CRD ops on order"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Limit orders to this user
        queryset = self.queryset.filter(user=self.request.user)
        # Allow to delete/cancel only not paid orders
        if self.action == "destroy":
            return queryset.filter(is_paid=False)
        return queryset

    def get_permissions(self):
        # Require address and cart items for order creation
        if self.action == "create":
            return [permission() for permission in self.permission_classes] + [
                DoesUserHaveAddress(),
                IsCartNotEmpty(),
            ]
        return super().get_permissions()


class PaymentView(APIView):
    """Manage payment creation"""

    permission_classes = [IsAuthenticated, IsOrderNotPaid]
    authentication_classes = [TokenAuthentication]

    Configuration.account_id = ""
    Configuration.secret_key = ""

    def post(self, request, order_pk):
        order = get_object_or_404(Order, pk=order_pk)
        payment = Payment.create(
            {
                "amount": {"value": order.total, "currency": order.currency},
                "confirmation": {
                    "type": "redirect",
                    "return_url": "http://localhost:8000/api/docs/",
                },
                "capture": True,
                "description": f"Оплата заказа №{order.id} для {request.user.email}",
            },
            uuid.uuid4(),
        )
        print(payment)
