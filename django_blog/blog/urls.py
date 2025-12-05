from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    TagListView, TagPostsView
)

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post CRUD
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Tag functionality
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', TagPostsView.as_view(), name='tag-posts'),
    
    # Search functionality - Using function-based view
    path('search/', views.search_posts, name='search'),
    
    # Comment CRUD
    path('post/<int:pk>/comments/new/', 
         CommentCreateView.as_view(), 
         name='comment-create'),
    path('comment/<int:pk>/update/', 
         CommentUpdateView.as_view(), 
         name='comment-update'),
    path('comment/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment-delete'),
]
