from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['room', 'name', 'email', 'persons', 'check_in', 'check_out']

        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'persons': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'check_in': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'check_out': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }