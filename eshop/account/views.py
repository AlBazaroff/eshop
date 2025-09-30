from django.shortcuts import render, HttpResponse
from django.contrib.auth import views as auth_views

from .forms import EmailAuthenticationForm

class LoginView(auth_views.LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'account/login.html'