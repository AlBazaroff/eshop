from django.urls import path

from . import views
from .application import webhooks

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('complete/', views.payment_completed, name='completed'),
    path('cancel/', views.payment_canceled, name='canceled'),
    # webhook
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook')
]