from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Custom form for user creation (signup) as UserCreationForm: only handles the default User model fields.
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
        model = User  # This means the form will save data to the User model, not Profile
        fields = ('username', 'password1', 'password2', 'phone_number', 'address', 'profile_photo')
        # These are the fields that will be included in the form.
        # The first three belong to the User model.
        # The last three are custom fields added to the form (not part of the User model).

# Form for editing the Profile model
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'profile_photo']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1, 'cols': 4}),
        }
