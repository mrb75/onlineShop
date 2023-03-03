from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

urlpatterns = [
    path('getCart', GetCart.as_view()),
    path('addToCart', AddToCart.as_view()),
    path('saveOrder', SaveOrder.as_view())
]

urlpatterns += router.urls
