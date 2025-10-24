from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
                                      PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import User, Profile
from utils.forms_utils import FormControlMixin

class PhoneInput(forms.TextInput):
    """
    Field for phone input validation by existing phone numbers
    """
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'pattern': r'^\+?1?\d{9,15}$',
            'title': "Phone number must be in format: '+999999999'."\
                "Up to 15 digits allowed."
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class PostalCodeInput(forms.TextInput):
    """
    Field for postal code input validation by existing postal codes
    """
    def __init__(self, attrs=None):
        default_attrs = {
            'pattern': r'^[0-9A-Za-z\s\-]{4,10}$',
            'title': 'You need to write exist postal code',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class EmailAuthenticationForm(FormControlMixin, AuthenticationForm):
    """
    Login user by email form
    change username field to email field
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            # 'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )

class UserRegistrationForm(FormControlMixin, UserCreationForm):
    """
    Form for user register with email, name and password
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your second name',
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
        super().__init__(ph=False, *args, **kwargs)

class EmailPasswordResetForm(PasswordResetForm):
    """ 
    Reset password by email
    """
    def get_users(self, email):
        """
        Get user model by email
        Args:
            email: user email
        """
        User = get_user_model()
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        return active_users
    
class EditUserForm(FormControlMixin, forms.ModelForm):
    """
    Edit user data form
    """
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(ph=False, *args, **kwargs)

class EditProfileForm(FormControlMixin, forms.ModelForm):
    """
    Edit users profile
    set up phone and postal_code fields
    for manage input
    """
    phone = forms.CharField(
        widget=PhoneInput,
        label='Phone',
        required=False,
    )
    postal_code = forms.CharField(
        widget=PostalCodeInput,
        label='Postal code',
        required=False,
    )
    class Meta:
        model = Profile
        fields = ['phone', 'city', 'address', 'postal_code']

class EmailPasswordChangeForm(FormControlMixin, PasswordChangeForm):
    """
    Change password by email with Mixin
    to set up
    """
    pass