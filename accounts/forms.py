from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Used for account verification")
    phone_number = forms.CharField(max_length=15, required=True, help_text="Used by buyers to contact you via phone or WhatsApp")
    hostel_location = forms.CharField(max_length=100, required=True, help_text="e.g., Hall 1, Main Campus, or Off-Campus")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'hostel_location')

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded-md'}))