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


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Retrieve or create the profile
            profile, created = Profile.objects.get_or_create(user=user)

            # Update the profile with additional fields
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.address = form.cleaned_data.get('address')
            profile.profile_photo = form.cleaned_data.get('profile_photo')
            profile.save()

            return redirect('login')  # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
# Login view

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Check if the user's profile is complete
            profile = user.profile
            if not profile.phone_number or not profile.address:
                return redirect('edit_profile')  # Redirect to edit profile if incomplete
            return redirect('dashboard')  # Redirect to dashboard if complete
        else:
            # Invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')  # Redirect to the login page after logout

# Dashboard view for logged-in users
@login_required  # Ensure only authenticated users can access the dashboard
@login_required
def dashboard_view(request):
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'phone_number': request.user.profile.phone_number,
        'address': request.user.profile.address,
        'profile_photo': request.user.profile.profile_photo,
    }
    return render(request, 'dashboard.html', context)
# Edit Profile view
@login_required
def edit_profile_view(request):
    profile = request.user.profile  # Retrieve the logged-in user's profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})