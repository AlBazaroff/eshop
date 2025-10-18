from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    """
    Order create form
    for guests and authorized user
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'city', 'address', 'postal_code']
        
    def __init__(self, user, profile, *args, **kwargs):
        """
        Initialize form fields
        Set up field for bootstrap class
        Initialize user data if authorized

        Args:
            user: user model if user is authorized
            profile: add profile data if user is authorized
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        if user and user.is_authenticated:
            # add for fields initial values
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone'].initial = profile.phone
            self.fields['city'].initial = profile.city
            self.fields['address'].initial = profile.address
            self.fields['postal_code'].initial = profile.postal_code
