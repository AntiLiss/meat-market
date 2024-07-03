from django.shortcuts import render
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from .permissions import DoesUserHaveAddress, IsCartNotEmpty


class OrderViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """Manage CRD ops on order"""

    permission_classes = [IsAuthenticated, DoesUserHaveAddress, IsCartNotEmpty]
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
