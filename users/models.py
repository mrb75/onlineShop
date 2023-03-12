from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import jdatetime
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator
from django.utils import timezone
from orders.models import Cart


class Country(models.Model):
    name = models.CharField(max_length=30)
    phone_code = models.CharField(max_length=5)


class Province(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(
        Country, models.CASCADE, related_name='provinces')
    slug = models.CharField(max_length=30, null=True, blank=True)


class City(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(
        Province, models.CASCADE, related_name='cities')
    slug = models.CharField(max_length=30, null=True, blank=True)


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'Male', _('مرد')
        FEMALE = 'Female', _('زن')
        NOTHING = 'Nothing', _('هیچکدام')
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(unique=True, null=True,
                              blank=True, max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    city = models.ForeignKey(City, models.CASCADE,
                             related_name='users', null=True, blank=True)
    national_code = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    gender = models.CharField(choices=Gender.choices,
                              default=Gender.NOTHING, max_length=10)
    credit = models.BigIntegerField(default=0)
    point = models.IntegerField(default=0)
    saved_products = models.ManyToManyField('products.Product')

    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_joined']

    @property
    def create_date_time(self):
        return datetime.datetime.strftime(self.date_joined, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_joined).strftime('%Y/%m/%d %H:%M'))

    @property
    def modify_date_time(self):
        return datetime.datetime.strftime(self.date_modified, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_modified).strftime('%Y/%m/%d %H:%M'))

    @property
    def current_cart(self):
        cart = Cart.objects.filter(user=self).last()
        if timezone.now() > cart.date_created+datetime.timedelta(days=7):
            cart = None

        return cart


class UserImage(models.Model):
    path = models.ImageField(upload_to='files/images')
    user = models.ForeignKey(User, models.CASCADE, related_name='images')
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


class Ticket(models.Model):
    class Type(models.TextChoices):
        SUPPORT = 'Support', _('پشتیبانی')
        COMPLAINS = 'Complains', _('شکایات')
        SUGGESTION = 'Suggestions', _('انتقادات و پیشنهادات')

    class State(models.TextChoices):
        CLOSED = 'Closed', _('بسته شده')
        OPEN = 'Pending', _('در حال بررسی')
        INIT = 'Waiting', _('در انتظار بررسی')

    message_type = models.CharField(
        choices=Type.choices, default=Type.SUGGESTION, max_length=30)
    subject = models.CharField(max_length=255)
    user = models.ForeignKey(User, models.CASCADE, related_name='tickets')
    status = models.CharField(
        choices=State.choices, default=State.INIT, max_length=30)
    text = models.TextField(max_length=20000)
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


class Address(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='addresses')
    text = models.TextField()
    lat = models.CharField(max_length=30, null=True, blank=True)
    long = models.CharField(max_length=30, null=True, blank=True)
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


class RequestLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requestLogs', null=True)
    ip_address = models.GenericIPAddressField()
    referer = models.CharField(max_length=255, null=True)
    user_agent = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    method = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_created']

    @property
    def create_date_time(self):
        return datetime.datetime.strftime(self.date_created, '%Y/%m/%d %H:%M'), _(jdatetime.datetime.fromgregorian(date=self.date_created).strftime('%Y/%m/%d %H:%M'))


class Notification(models.Model):
    user = models.ForeignKey(User, models.CASCADE,
                             related_name='notifications')
    is_news = models.BooleanField(default=False)
    text = models.TextField(max_length=1000)
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
