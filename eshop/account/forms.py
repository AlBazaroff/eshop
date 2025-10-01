from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
                                      PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import User

class FormControlMixin:
    """ Mixin for adding bootstrap classes"""
    def __init__(self, placeholder=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if placeholder:
                field.widget.attrs['placeholder'] = f'Enter your {field.label.lower()}'

class EmailAuthenticationForm(FormControlMixin, AuthenticationForm):
    """ User login form """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            # 'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )

class UserRegistrationForm(FormControlMixin, UserCreationForm):
    """ Form for user register"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(placeholder=False, *args, **kwargs)

class EmailPasswordResetForm(PasswordResetForm):
    """ 
    Password reset by email
    """
    def get_users(self, email):
        User = get_user_model()
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        return active_users
    
class EditUserForm(FormControlMixin, forms.ModelForm):
    """
    Edit user information
    """
    email = forms.EmailField()

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(placeholder=False, *args, **kwargs)

class EmailPasswordChangeForm(FormControlMixin, PasswordChangeForm):
    """
    Change password by email
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)