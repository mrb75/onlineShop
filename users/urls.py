
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'favorites', FavoriteViewSet, basename='favoriteProduct')
urlpatterns = [
    path('register', Register.as_view()),
    path('editProfile', EditProfile.as_view()),
    path('profile', Profile.as_view())
]
urlpatterns += router.urls
