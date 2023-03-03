from django.db import models
import datetime
import jdatetime
from django.utils.translation import gettext as _


class Cart(models.Model):
    products = models.ManyToManyField(
        'products.Product', through='CartProduct')
    user = models.ForeignKey(
        'users.User', models.CASCADE, null=True, blank=True)
    cookie_value = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']

    @property
    def create_date_time(self):
        return datetime.datetime.strftime(self.date_created, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_created).strftime('%Y/%m/%d %H:%M'))

    @property
    def modify_date_time(self):
        return datetime.datetime.strftime(self.date_modified, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_modified).strftime('%Y/%m/%d %H:%M'))

    @property
    def total_price(self):
        for item in self.cartproduct_set.all():
            item_product = item.product.productcolor_set.filter(
                color=item.color).last()
            if hasattr(item_product, "price"):
                yield item_product.price
            else:
                yield item.product.price

        # return price


class CartProduct(models.Model):
    product = models.ForeignKey('products.Product', models.CASCADE)
    cart = models.ForeignKey(Cart, models.CASCADE)
    number = models.IntegerField(default=1)
    color = models.ForeignKey(
        'products.Color', models.CASCADE, null=True, blank=True)


class Order(models.Model):
    user = models.ForeignKey(
        'users.User', models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart, models.CASCADE)
    mobile = models.CharField(max_length=14)
    postage_cost = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    delivery_date = models.DateTimeField()
    address = models.TextField()
    lat = models.CharField(max_length=30, null=True, blank=True)
    long = models.CharField(max_length=30, null=True, blank=True)
    city = models.ForeignKey('users.City', models.CASCADE)
    recipient = models.CharField(max_length=30, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']

    @property
    def delivery_date_time(self):
        return datetime.datetime.strftime(self.delivery_date, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.delivery_date).strftime('%Y/%m/%d %H:%M'))

    @property
    def create_date_time(self):
        return datetime.datetime.strftime(self.date_created, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_created).strftime('%Y/%m/%d %H:%M'))

    @property
    def modify_date_time(self):
        return datetime.datetime.strftime(self.date_modified, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_modified).strftime('%Y/%m/%d %H:%M'))
