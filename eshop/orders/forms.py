from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    """
    Form for creation orders
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email',
                  'phone', 'city', 'address', 'postal_code']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
