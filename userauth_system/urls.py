from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Redirect the root URL to the signup page
    path('', lambda request: redirect('signup')),  # Redirect to 'signup'

    # Include userprofile app URLs
    path('userprofile/', include('userprofile.urls')),  # Delegate URLs to userprofile
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)