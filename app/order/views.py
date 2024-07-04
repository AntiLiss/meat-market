import os
import uuid
import yookassa
import json
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer, PaymentCreateSerializer
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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at"]
    filterset_fields = ["is_paid"]

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


yookassa.Configuration.account_id = os.environ.get("YOOKASSA_ACCOUNT_ID")
yookassa.Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")


class PaymentCreateView(APIView):
    """Manage payment creation"""

    permission_classes = [IsAuthenticated, IsOrderNotPaid]
    authentication_classes = [TokenAuthentication]
    serializer_class = PaymentCreateSerializer

    def post(self, request, order_pk):
        order = get_object_or_404(Order, pk=order_pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_url = serializer.validated_data.get("return_url")
        payment = yookassa.Payment.create(
            {
                "amount": {
                    "value": order.total,
                    "currency": "RUB",
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url,
                },
                "capture": True,
                "description": f"Оплата заказа №{order.id} для {order.user.email}",
                "metadata": {"order_id": order.id},
            },
            uuid.uuid4(),
        )
        return Response(payment)


class PaymentAcceptView(APIView):
    """Modify order depending on the payment status"""

    def post(self, request):
        notification = json.loads(request.body)
        # If payment succeeded mark the order as paid
        if notification["event"] == "payment.succeeded":
            order_id = notification["object"]["metadata"]["order_id"]
            order = get_object_or_404(Order, pk=order_id)
            order.is_paid = True
            order.save()

        print(notification)
        return Response(status=200)
