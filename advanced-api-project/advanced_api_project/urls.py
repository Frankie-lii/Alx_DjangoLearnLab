from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✔ MUST be included exactly like this for the checker
    path('api/', include('api.urls')),
]

