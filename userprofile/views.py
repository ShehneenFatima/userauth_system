from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from .forms import CustomUserCreationForm

# Signup view


def signup_view(request): # This function handles the signup page (both showing the form and saving the data).
    if request.method == 'POST': # If the user submitted the form (clicked the signup button), handle the submitted data.
        form = CustomUserCreationForm(request.POST, request.FILES) # Create a form instance filled with the submitted data (text and files like images).

        if form.is_valid():  # Check if the submitted data is correct and safe (no errors, valid input).

            
            user = form.save() # Save the new user to the database (creates a new User object).

            
            profile, created = Profile.objects.get_or_create(user=user) # Check if the user already has a profile.
            # If not, create a new Profile object linked to the user.
            # Update the profile with additional fields
            profile.phone_number = form.cleaned_data.get('phone_number') # Get the cleaned phone number from the form and save it to the profile.
            profile.address = form.cleaned_data.get('address')# Get the cleaned address from the form and save it to the profile.
            profile.profile_photo = form.cleaned_data.get('profile_photo')# Get the uploaded profile photo from the form and save it to the profile.

            profile.save()# Save the profile to the database with the updated information.

            return redirect('login')  # After successful signup, redirect the user to the login page.
    else:# If the user is just opening the signup page (GET request), create an empty form.
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})  # Render the 'signup.html' template and pass the form to it so it shows on the page.

# Login view

def login_view(request):# This function handles the login logic when a user visits or submits the login form.
    if request.method == 'POST':# If the form is submitted (POST request), then process the login.

        username = request.POST.get('username')# Get the username entered by the user from the form.
        password = request.POST.get('password')# Get the password entered by the user from the form.
        user = authenticate(request, username=username, password=password)# Check if a user exists with the given username and password.
        # If correct, `user` will be a User object. If not, `user` will be None.

        if user is not None:
            login(request, user)# Log the user in (create a session).

            # Check if the user's profile is complete
            profile = user.profile# Access the profile related to the logged-in user.
            if not profile.phone_number or not profile.address or not profile.profile_photo: #If phone number or address is missing, redirect the user to edit their profile.
                return redirect('edit_profile')  # Redirect to edit profile if incomplete
            return redirect('dashboard') # If profile is complete, redirect the user to their dashboard.
        else:
            # Invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})# If authentication failed, reload the login page and show an error message.

    return render(request, 'login.html') # If the page is opened with a GET request (i.e., no form submitted yet),
    # show the empty login form.



# Logout view
@login_required # This decorator ensures that only logged-in users can access this view
def logout_view(request): 
    logout(request) # Log the user out (clear their session)
    messages.success(request, "Logged out successfully!")  # Show a success message to the user
    return redirect('login')  # Redirect to the login page after logout

# Dashboard view for logged-in users
# Ensure only authenticated users can access the dashboard
@login_required  # Only logged-in users can access the dashboard
def dashboard_view(request):
    context = {
        'username': request.user.username,  # Get the logged-in user's username
        'phone_number': request.user.profile.phone_number,  # Get phone number from profile
        'address': request.user.profile.address,  # Get address from profile
        'profile_photo': request.user.profile.profile_photo,  # Get profile photo
    }
    return render(request, 'dashboard.html', context)  # Show all this info in the dashboard page

# Edit Profile view
# Edit Profile view
@login_required  # Only logged-in users can edit their profile
def edit_profile_view(request):
    profile = request.user.profile  # Get the profile linked to the logged-in user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # If form is submitted, fill it with submitted data and files (like photo), connected to the existing profile

        if form.is_valid():
            form.save()  # Save the updated profile info
            return redirect('dashboard')  # After saving, go back to the dashboard
    else:
        form = ProfileForm(instance=profile)
        # If it's a GET request (user opened the page), show the form with current profile data pre-filled

    return render(request, 'edit_profile.html', {'form': form})
    # Show the edit form page to the user
