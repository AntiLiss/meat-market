from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductDiscountViewSet,
    ReviewViewSet,
)


app_name = "product"

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("discounts", ProductDiscountViewSet)

review_list_view = ReviewViewSet.as_view({"get": "list", "post": "create"})
review_detail_view = ReviewViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "products/<int:product_pk>/reviews/",
        review_list_view,
        name="review-list",
    ),
    path(
        "products/<int:product_pk>/reviews/<int:pk>/",
        review_detail_view,
        name="review-detail",
    ),
]
