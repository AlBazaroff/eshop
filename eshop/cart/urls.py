from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
     path('', views.cart_detail, name='detail'),
     # change cart items
     path('add/<int:product_id>/', views.add_cart,
          name='add_cart'),
     path('remove/<int:product_id>/', views.remove_cart,
          name='remove_cart'),
     path('clear/', views.clear_cart,
          name='clear_cart'),
]