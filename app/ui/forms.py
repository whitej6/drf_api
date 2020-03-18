from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from core.models import User, Restaurant


class BootstrapMixin(forms.BaseForm):
    """
    Add the base Bootstrap CSS classes to form elements.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exempt_widgets = [
            forms.CheckboxInput, forms.ClearableFileInput, forms.FileInput, forms.RadioSelect
        ]

        for field_name, field in self.fields.items():
            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()
            if field.required and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['required'] = 'required'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label


class LoginForm(BootstrapMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['password'].widget.attrs['placeholder'] = ''


class CreateUserForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name")


class RestaurantForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['user']
