from django.urls import path, include
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView
)

# Post URLs with singular "post"
post_patterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post URLs
    path('post/', include(post_patterns)),
    
    # Also support plural "posts" for backward compatibility
    path('posts/', PostListView.as_view(), name='posts-list'),
    path('posts/new/', PostCreateView.as_view(), name='posts-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='posts-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='posts-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='posts-delete'),
]
