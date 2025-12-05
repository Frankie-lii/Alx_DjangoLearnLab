from django.urls import path
from . import views

urlpatterns = [
    # Basic URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Post URLs
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    # Tag URLs
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', views.TagPostsView.as_view(), name='tag-posts'),
    
    # Search URL - CRITICAL for "Develop Search Functionality" task
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Comment URLs
    path('post/<int:pk>/comments/new/', 
         views.CommentCreateView.as_view(), 
         name='comment-create'),
    path('comment/<int:pk>/update/', 
         views.CommentUpdateView.as_view(), 
         name='comment-update'),
    path('comment/<int:pk>/delete/', 
         views.CommentDeleteView.as_view(), 
         name='comment-delete'),
]
