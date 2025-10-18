from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    """
    Form for edit or update Product model
    set up elements for bootstrap
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'category',
                  'image', 'price', 'available']
        
    def __init__(self, *args, **kwargs):
        """
        Initialize form elements
        set up fields class
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'