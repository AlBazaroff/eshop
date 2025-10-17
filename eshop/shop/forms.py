from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    """
    Form for edit or update
    model product
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'category',
                  'image', 'price', 'available']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'