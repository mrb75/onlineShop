from django.db.models.signals import post_save
from django.dispatch import receiver
from . import tasks
from .models import Order


@receiver(post_save, sender=Order)
def send_order_ship_notification(sender, **kwargs):
    print('saved')
    if kwargs['created']:
        print('created')
        tasks.orderSaved(kwargs['instance'])
