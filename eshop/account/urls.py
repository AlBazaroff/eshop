from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', views.custom_logout, name='logout'),
     path('password-change/', auth_views.PasswordChangeView.as_view(),
          name='password_change'),
     path('password-reset/', auth_views.PasswordResetView.as_view(),
          name='password_reset'),
     path('register/', views.register, name='register'),
]