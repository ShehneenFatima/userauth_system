from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('accounts/login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('accounts/dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard page
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),  # Edit profile page
]