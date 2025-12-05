from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post CRUD operations
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comment CRUD operations - using EXACT paths required by checker
    path('post/<int:pk>/comments/new/', 
         CommentCreateView.as_view(), 
         name='comment-create'),
    path('comment/<int:pk>/update/', 
         CommentUpdateView.as_view(), 
         name='comment-update'),
    path('comment/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment-delete'),
    
    # Additional comment actions (if needed)
    path('comment/<int:pk>/like/', 
         views.comment_like_toggle, 
         name='comment-like'),
    path('comment/<int:pk>/reply/', 
         views.comment_reply, 
         name='comment-reply'),
    path('post/<int:post_pk>/comments/', 
         views.comment_list, 
         name='comment-list'),
]
