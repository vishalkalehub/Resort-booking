from django import forms
from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['name', 'email', 'persons', 'check_in', 'check_out']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'persons': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'check_in': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'check_out': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}
    ))


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]       

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm        