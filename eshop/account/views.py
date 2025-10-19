from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, update_session_auth_hash, \
    views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import EmailAuthenticationForm, UserRegistrationForm, \
    EmailPasswordResetForm, EditUserForm, EmailPasswordChangeForm, \
    EditProfileForm
from .user_orders import order_list, order_detail
from .models import Profile

class LoginView(auth_views.LoginView):
    """
    Login users by email
    """
    form_class = EmailAuthenticationForm
    template_name = 'account/register/login.html'

@login_required
def custom_logout(request):
    """
    User logout
    """
    logout(request)
    return redirect('shop:product_list')

def register(request):
    """
    Custom registration by email
    """
    if request.user.is_authenticated:
        redirect('shop:product_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = UserRegistrationForm()

    return render(request,
                  'account/register/register.html',
                  {'register_form': form})

@login_required
def edit_user(request):
    """
    View edit user
    edit email, first_name, last_name
    """
    if request.method == 'POST':
        user_form = EditUserForm(data=request.POST, instance=request.user)
        profile_form = EditProfileForm(data=request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('shop:product_list')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request,
                  'account/edit_user.html',
                  {'edit_user_form': user_form,
                   'edit_profile_form': profile_form})

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

@staff_member_required
def admin_menu(request):
    """
    Admin menu in account settings
    """
    return render(request,
                  'account/admin/admin_menu.html')


class PasswordResetView(auth_views.PasswordResetView):
    """
    View for reset password by email
    """
    form_class = EmailPasswordResetForm
    template_name = 'account/register/password_reset.html'
    email_template_name = 'account/register/password_reset_email.html'
    success_url = '/password-reset/done/'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    View for reset done
    """
    template_name = 'account/register/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    Confirmation reset
    """
    form_class = SetPasswordForm
    template_name = 'account/register/password_reset_confirm.html'
    success_url = '/reset/done/'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """
    Complete password reset
    """
    template_name = 'account/register/password_reset_complete.html'