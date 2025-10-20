#!forms_utils.py
class FormControlMixin:
    """
    Mixin for set up form elements
    and add classes for bootstrap
    Args:
        ph: add placeholder if ph = True
    """
    def __init__(self, *args, ph = True, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if ph:
                field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'