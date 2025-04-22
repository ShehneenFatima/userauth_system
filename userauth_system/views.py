from django.shortcuts import render, redirect

# Homepage view
def home_view(request):
    """
    Renders the homepage. If the user is authenticated, they are redirected to the dashboard.
    Otherwise, they are redirected to the signup page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect authenticated users to the dashboard
    else:
        return redirect('signup')  # Redirect unauthenticated users to the signup page