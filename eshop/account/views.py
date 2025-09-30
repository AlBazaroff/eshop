from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

from .forms import EmailAuthenticationForm
from . import views

class LoginView(auth_views.LoginView):
    """
    Login
    """
    form_class = EmailAuthenticationForm
    template_name = 'account/login.html'

def custom_logout(request):
    " custom logout "
    logout(request)
    return redirect('shop:product_list')