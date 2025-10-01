from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, views as auth_views
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, \
    SetPasswordForm
from django.contrib.auth.decorators import login_required

from .forms import EmailAuthenticationForm, UserRegistrationForm, \
    EmailPasswordResetForm

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

class PasswordResetView(auth_views.PasswordResetView):
    """ View for reset password by email """
    form_class = EmailPasswordResetForm
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    success_url = '/password-reset/done/'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """ View for reset done  """
    template_name = 'account/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """ Confirmation reset """
    form_class = SetPasswordForm
    template_name = 'account/password_reset_confirm.html'
    success_url = '/reset/done/'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """ Complete password reset"""
    template_name = 'account/password_reset_complete.html'