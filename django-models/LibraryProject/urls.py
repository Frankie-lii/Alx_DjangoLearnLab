#!/usr/bin/env python3
from django.contrib import admin
from django.urls import path, include
from .views import list_books
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
]

