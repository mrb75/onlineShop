from rest_framework import serializers
from products.models import Product, Color
from .models import Cart, Order, CartProduct
from products.serializers import ProductSerializer
from users.serializers import AddressSerializer
import jdatetime
from datetime import datetime, timedelta
from django.utils import timezone


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['color', 'number', 'product']
        depth = 1


class CartSerializer(serializers.ModelSerializer):
    cartproduct_set = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id',  'cookie_value', 'total_price', 'cartproduct_set',
                  'create_date_time', 'modify_date_time']
        depth = 1


class CartFormSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    number = serializers.IntegerField(default=1)
    color_id = serializers.IntegerField(allow_null=True, default=0)

    def validate_product_id(self, value):
        if len(Product.objects.filter(id=value)) <= 0:
            raise serializers.ValidationError("Product is not valid.")
        return value

    def validate_color_id(self, value):
        if len(Color.objects.filter(id=value)) <= 0 and value != 0:
            raise serializers.ValidationError("Color is not valid.")
        return value

    def validate(self, attrs):
        has_product = 'product_id' in attrs
        has_color = 'color_id' in attrs
        if has_product ^ has_color:
            raise serializers.ValidationError(
                "product and color would be determind with each other")
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    address_field = serializers.IntegerField()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['user', 'cart', 'city', 'address', 'delivery_date']

    def validate_address_field(self, val):
        if not (self.context['request'].user.addresses.get(pk=val)):
            raise serializers.ValidationError("address is invalid")
        return val

    def create(self, validated_data):
        user = self.context['request'].user
        address_field_id = validated_data.pop("address_field")
        order = Order(**validated_data)
        address_field = user.addresses.get(pk=address_field_id)
        order.user = user
        order.cart = user.current_cart
        order.city = user.city
        order.address = address_field.text
        order.lat = address_field.lat
        order.long = address_field.long
        order.delivery_date = timezone.datetime.now() + timedelta(days=2)
        order.save()
        return order


class OrderShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["mobile", "postage_cost", "cost", "delivery_date", "address",
                  "lat", "long", "cart", "city", "create_date_time", "modify_date_time"]
        depth = 1
