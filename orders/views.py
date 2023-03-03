from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import CartSerializer, CartFormSerializer, OrderSerializer
from .filters import *
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from products.models import Product, Color
from django.utils import timezone


class AddToCart(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def post(self, request):
        cart_form_serializer = CartFormSerializer(data=request.data)
        if cart_form_serializer.is_valid():
            if 'cart' in request.COOKIES:
                cart = Cart.objects.filter(
                    cookie_value=request.COOKIES['cart']).last()
            else:
                cart = Cart.objects.filter(
                    user=request.user).last()
            now = datetime.now()
            if not (cart) or timezone.now() > cart.date_created+timedelta(days=7):
                cart = Cart.objects.create(cookie_value=now, user=request.user)
            product = Product.objects.get(
                pk=cart_form_serializer.data['product_id'])
            products = cart.products.all()
            if not (product in products):
                cart.products.add(product, through_defaults={
                                  'color': Color.objects.filter(id=cart_form_serializer.data['color_id']).last()})
            else:
                cart_option = CartProduct.objects.filter(
                    cart=cart, product=product).first()
                cart_option.number += 1
                cart_option.save()
            cart.cookie_value = now
            cart.save()
            response = Response()
            response.set_cookie(
                "cart", now, (now+timedelta(days=7)).timestamp())
            return response
        else:
            return Response(cart_form_serializer.errors, 400)


class GetCart(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get(self, request):
        if 'cart' in request.COOKIES:
            cart = Cart.objects.filter(
                cookie_value=request.COOKIES['cart']).last()
        else:
            cart = Cart.objects.filter(user=request.user).last()
        if not (cart) or timezone.now() > cart.date_created+timedelta(days=7):
            return Response()
        return Response(CartSerializer(cart).data)


class SaveOrder(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def post(self, request):
        order_serializer = OrderSerializer(
            data=request.data, context={'request': request})
        if order_serializer.is_valid():
            order = order_serializer.create(request.data)
            return Response(status=201)
        else:
            return Response(order_serializer.errors, status=400)
