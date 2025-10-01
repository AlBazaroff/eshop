from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, views as auth_views
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import EmailAuthenticationForm, UserRegistrationForm

class LoginView(auth_views.LoginView):
    """
    Login
    """
    form_class = EmailAuthenticationForm
    template_name = 'account/login.html'

@login_required
def custom_logout(request):
    " custom logout "
    logout(request)
    return redirect('shop:product_list')

class PasswordResetView(auth_views.PasswordResetView):
    """
    View for password reset
    """
    form_class = PasswordResetForm
    template_name = 'account/password_reset.html'

class PasswordChangeForm(auth_views.PasswordChangeView):
    """
    View for password change
    """
    form_class = PasswordChangeForm
    template_name = 'account/password_change.html'

def register(request):
    if request.user.is_authenticated:
        redirect('shop:product_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'register_form': form})