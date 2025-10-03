from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    """
    Form for creation orders
    """
    postal_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': r'^[A-Z0-9\- ]{4,10}$',
            'title': "Your index isn't valid. Input correct index"
            }
        )
    )
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'city', 'address', 'postal_code']
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone'].initial = user.phone