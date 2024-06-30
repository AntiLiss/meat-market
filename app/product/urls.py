from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductDiscountViewSet,
    ReviewListView,
    ReviewDetailView,
)


app_name = "product"

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("discounts", ProductDiscountViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "products/<int:product_pk>/reviews/",
        ReviewListView.as_view(),
        name="review-list",
    ),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]
