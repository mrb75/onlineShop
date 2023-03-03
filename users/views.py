from django.shortcuts import render
from rest_framework.views import APIView
from onlineShop.permissions import IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, RegisterSerializer, UserFormSerializer, AddressSerializer, TicketSerializer
from .models import User, Address
from rest_framework.response import Response
from orders.serializers import OrderShowSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from products.serializers import CommentSerializer, ProductSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin


class Register(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        register_serializer = RegisterSerializer(data=request.data)
        if (register_serializer.is_valid()):

            user_data = register_serializer.data
            user_data.pop("password_confirmation")
            password = user_data.pop("password")
            user = User(**user_data)
            user.set_password(password)
            user.save()
            return Response(status=200)
        else:
            return Response(register_serializer.errors, 400)


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class EditProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def patch(self, request):
        user_serializer = UserFormSerializer(request.user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, 204)
        else:
            return Response(user_serializer.errors, 400)


class OrderViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = OrderShowSerializer

    def get_queryset(self):
        return self.request.user.orders.all()


class AddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.request.user.addresses.all()


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.request.user.comments.all()


class TicketViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return self.request.user.tickets.all()


class FavoriteViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.saved_products.all()
