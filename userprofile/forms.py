from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Custom form for user creation (signup)
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Enter your phone number (e.g., +1234567890)."
    )
    address = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Enter your address."
    )
    profile_photo = forms.ImageField(
        required=False,
        help_text="Upload your profile photo."
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'phone_number', 'address', 'profile_photo')

# Form for editing the Profile model
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'profile_photo']