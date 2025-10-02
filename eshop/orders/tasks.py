from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Order

@shared_task
def order_created(order_id):
    """
    Task for send email
    after success order created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order no. {order.id}'
    message = f'Your order has been successfully created. ' \
              f'Order id is {order.id}. Thanks'
    mail = send_mail(subject,
                     message,
                     None,
                     recipient_list=[order.email])
    return mail