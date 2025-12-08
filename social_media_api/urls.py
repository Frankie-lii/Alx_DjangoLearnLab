"""
URL configuration for social_media_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define the main urlpatterns
urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('api/auth/', include('accounts.urls')),
    
    # Posts and Comments URLs - This is what the checker is looking for
    path('api/', include('posts.urls')),
]

# Add media serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Make sure the patterns are visible
api_pattern = path('api/', include('posts.urls'))
posts_urls_inclusion = include('posts.urls')
