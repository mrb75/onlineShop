from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ChangeProductFavorite
from django.urls import path
router = DefaultRouter()


router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
urlpatterns = [
    path("changeProductFavorite", ChangeProductFavorite.as_view())
]
urlpatterns += router.urls
