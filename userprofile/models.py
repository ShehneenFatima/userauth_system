from django.db import models
from django.contrib.auth.models import User # Importing the built-in User model from Django to link the profile to a user.
from django.core.validators import RegexValidator# Importing RegexValidator to validate the phone number format.

class Profile(models.Model):# This is the Profile model that holds additional data for each user.
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
     # This links the Profile to the User model with a One-to-One relationship.
    # Each user will have only one profile, and each profile will be linked to one user.
    # If the user is deleted, the profile will be deleted as well (CASCADE).
    # The 'unique=True' ensures that no two profiles can be linked to the same user.


    phone_number = models.CharField(
        max_length=15,
        blank=True,# The phone number is not optional (cannot be left blank in forms).
        null=True,#The phone number cannot be NULL in the database if not provided.
        validators=[
            RegexValidator( # Applying a validation to the phone number format.
                regex=r'^\+?[0-9]{10,15}$',
                message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Enter your phone number (e.g., +1234567890)."# Help text shown to the user on the form, giving an example of the correct phone number format.
    )
    address = models.TextField(blank=True, null=True, help_text="Enter your address.") # This field stores the user's address. It's optional and can be left blank in the form or NULL in the database.
    # It's a TextField because the address might be long, and TextField allows for larger content than CharField.
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, help_text="Upload your profile photo.")# The uploaded photo will be stored in the 'profile_photos/' directory under the media folder.

    def __str__(self):# This method defines what will be shown when a Profile object is printed (e.g., in the Django admin).
        return f"{self.user.username}'s Profile" 
    # It will return the user's username followed by 'Profile' (e.g., 'shehneen' Profile').

