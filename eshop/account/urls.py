from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', views.custom_logout, name='logout'),
     path('register/', views.register, name='register'),
     path('account/edit-user', views.edit_user, name='edit_user'),
     # password reset urls
     path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
     path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('password-change/', views.password_change, name='password_change')
]