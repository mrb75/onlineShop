from rest_framework import serializers
from .models import Category, Product, Color, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'create_date_time', 'modify_date_time']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'price', 'discount', 'description',
                  'create_date_time', 'modify_date_time', 'seller', 'category', 'properties', 'colors']
        depth = 1


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'product', 'text', 'create_date_time',
                  'modify_date_time', 'verify_date_time']

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.user = self.context['request'].user
        comment.save()
        return comment

    def update(self, instance, validated_data):
        comment = super().update(instance, validated_data)
        comment.date_verified = None
        comment.save()
        return comment


class FavoriteSerializer(serializers.Serializer):
    product = serializers.IntegerField()

    def validate_product(self, value):
        if len(Product.objects.filter(id=value)) <= 0:
            raise serializers.ValidationError("Product is not valid.")
        return value
