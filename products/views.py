from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Category
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import CategorySerializer, ProductSerializer, FavoriteSerializer
from .filters import *
from rest_framework.views import APIView
from rest_framework.response import Response


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        if 'parent' in self.request.query_params:
            return Category.objects.filter(parent__id=self.request.query_params['parent'])
        return Category.objects.filter(parent__isnull=True)

    def list(self, request):
        return super().list(request)

    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        if 'category' in self.request.query_params:
            return Category.objects.get(pk=self.request.query_params['category']).products
        return Product.objects.all()

    @method_decorator(cache_page(60*30))
    def list(self, request):
        return super().list(request)

    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ChangeProductFavorite(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def post(self, request):
        favorite_srializer = FavoriteSerializer(data=request.data)
        if favorite_srializer.is_valid():
            product = Product.objects.get(pk=request.data['product'])
            if not (request.user.saved_products.filter(id=product.id)):
                request.user.saved_products.add(product)
            else:
                request.user.saved_products.remove(product)

            return Response()
        else:
            return Response(favorite_srializer.errors, 400)
