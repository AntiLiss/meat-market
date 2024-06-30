from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, generics
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, ProductDiscount, Review
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDiscountSerializer,
    ReviewSerializer,
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


class ReviewListView(generics.ListCreateAPIView):
    """Review listing and creation"""

    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at", "rating"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        product_id = self.kwargs.get("product_pk")
        product = get_object_or_404(Product, pk=product_id)
        # Limit reviews to contextual product
        return self.queryset.filter(product=product)

    def get_permissions(self):
        # Allow only authenticated user to create review
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Set `user` to this user and `product` to this product
        product_id = self.kwargs.get("product_pk")
        product = get_object_or_404(Product, pk=product_id)
        return serializer.save(user=self.request.user, product=product)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Review detail read, update and delete operations"""

    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Allow user to edit only his reviews
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    def get_permissions(self):
        # Allow only authenticated user to edit review
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
