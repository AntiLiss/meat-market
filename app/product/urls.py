from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductDiscountViewSet


app_name = "product"

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("discounts", ProductDiscountViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
