from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from core.models import User, Restaurant


def get_state():
    restaurants = Restaurant.objects.all().distinct('state')
    choices = (('', '---------'),)
    for i in restaurants:
        choices += ((i.state, i.state),)
    return choices


def get_city():
    restaurants = Restaurant.objects.all().distinct('city')
    choices = (('', '---------'),)
    for i in restaurants:
        choices += ((i.city, i.city),)
    return choices


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


class SearchForm(BootstrapMixin, forms.Form):
    q = forms.CharField(
        label='Search',
        required=False
    )
    name = forms.CharField(
        label='Name',
        required=False
    )
    city = forms.ChoiceField(
        choices=get_city,
        label='City',
        required=False
    )
    state = forms.ChoiceField(
        choices=get_state,
        required=False,
        label='State'
    )
    zip_code = forms.CharField(
        label='Zip Code',
        required=False
    )
    dine_in = forms.BooleanField(
        label='Dine In',
        required=False
    )
    take_out = forms.BooleanField(
        label='Take Out',
        required=False
    )
    drive_thru = forms.BooleanField(
        label='Drive Thru',
        required=False
    )
    curbside = forms.BooleanField(
        label='Curside',
        required=False
    )
    delivery = forms.BooleanField(
        label='Delivery',
        required=False
    )
