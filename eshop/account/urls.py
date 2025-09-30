from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', views.custom_logout, name='logout'),
]