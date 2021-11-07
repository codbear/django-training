from django.forms import ModelForm, TextInput, EmailInput

from .models import Contacts


class BookingForm(ModelForm):
    class Meta:
        model = Contacts
        fields = ['name', 'email']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }
