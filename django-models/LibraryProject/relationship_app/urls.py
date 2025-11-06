from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Login
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Register
    path('register/', views.register, name='register'),

    # Optional: your existing book/library views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

