import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['contains'],
            'price':['exact','lte','gte'],
            'discount':['exact','lte','gte'],
            'description':['contains'],
            'seller':['exact'],
            'category':['exact'],
            'properties':['contains'],
            'colors':['contains']
        }