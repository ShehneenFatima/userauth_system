from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Enter your phone number (e.g., +1234567890)."
    )
    address = models.TextField(blank=True, null=True, help_text="Enter your address.")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, help_text="Upload your profile photo.")

    def __str__(self):
        return f"{self.user.username}'s Profile"