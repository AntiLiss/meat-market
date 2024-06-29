from rest_framework import filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, ProductDiscount
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDiscountSerializer,
)


class CategoryViewSet(ReadOnlyModelViewSet):
    """Manage category viewing (list, retrieve)"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ReadOnlyModelViewSet):
    """Manage product viewing (list, retrieve)"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at", "price", "rating"]
    filterset_fields = ["category"]  # Fields to filter by


class ProductDiscountViewSet(ReadOnlyModelViewSet):
    """Manage product discount viewing (list, retrieve)"""

    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscountSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]
