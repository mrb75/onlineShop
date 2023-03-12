from celery import shared_task
from orders.models import Order
from users.models import Notification


@shared_task
def orderSaved(order):
    Notification.objects.create(
        user=order.user, text='Your Order saved successfully.',)
