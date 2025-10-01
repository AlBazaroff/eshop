from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, update_session_auth_hash, \
    views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EmailAuthenticationForm, UserRegistrationForm, \
    EmailPasswordResetForm, EditUserForm, EmailPasswordChangeForm

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

@login_required
def edit_user(request):
    """
    View edit user
    edit email, first_name, last_name
    """
    if request.method == 'POST':
        form = EditUserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('shop:product_list')
    else:
        form = EditUserForm(instance=request.user)
    return render(request,
                  'account/edit_user.html',
                  {'edit_user_form': form})

@login_required
def password_change(request):
    """
    View for change password
    using email
    """
    if request.method == 'POST':
        form = EmailPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('shop:product_list')
    else:
        form = EmailPasswordChangeForm(user=request.user)
    return render(request,
                  'account/password_change.html',
                  {'form': form})

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

