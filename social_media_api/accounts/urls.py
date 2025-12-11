from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserDetailView,
    UserFollowView,
    UserFollowingListView,
    UserFollowersListView,
    UserListView
)

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # Profile endpoints
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    
    # Follow management endpoints
    path('follow/<int:user_id>/', UserFollowView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UserFollowView.as_view(), name='unfollow-user'),
    path('following/', UserFollowingListView.as_view(), name='following-list'),
    path('followers/', UserFollowersListView.as_view(), name='followers-list'),
    path('users/', UserListView.as_view(), name='user-list'),
]
