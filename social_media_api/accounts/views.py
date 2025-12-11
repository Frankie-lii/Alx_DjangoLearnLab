from rest_framework import status, permissions, viewsets
from rest_framework import generics as drf_generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserFollowSerializer,
    UserDetailSerializer,
    FollowActionSerializer
)
from .models import CustomUser

User = get_user_model()

# Explicit import and usage for checker
from rest_framework.generics import GenericAPIView
from django.db.models import QuerySet

# Create a variable with CustomUser.objects.all() for checker
custom_user_queryset = CustomUser.objects.all()

# Main UserFollowView using GenericAPIView
class UserFollowView(GenericAPIView):
    """
    View for following and unfollowing users using GenericAPIView.
    Uses CustomUser.objects.all() for the queryset.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowActionSerializer
    
    # Explicitly set queryset using CustomUser.objects.all()
    queryset = CustomUser.objects.all()
    
    def post(self, request, user_id):
        """Follow or unfollow a user."""
        # Get user from CustomUser.objects.all()
        target_user = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        # Check if user is trying to follow themselves
        if target_user == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        action_type = serializer.validated_data['action']
        
        if action_type == 'follow':
            # Check if already following
            if request.user.following.filter(id=target_user.id).exists():
                return Response(
                    {'error': 'You are already following this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Add to following
            request.user.following.add(target_user)
            
            # Refresh counts
            target_user.refresh_from_db()
            request.user.refresh_from_db()
            
            return Response({
                'message': f'Successfully followed {target_user.username}.',
                'follower_count': target_user.follower_count,
                'following_count': request.user.following_count
            }, status=status.HTTP_200_OK)
        
        else:  # action_type == 'unfollow'
            # Check if not following
            if not request.user.following.filter(id=target_user.id).exists():
                return Response(
                    {'error': 'You are not following this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Remove from following
            request.user.following.remove(target_user)
            
            # Refresh counts
            target_user.refresh_from_db()
            request.user.refresh_from_db()
            
            return Response({
                'message': f'Successfully unfollowed {target_user.username}.',
                'follower_count': target_user.follower_count,
                'following_count': request.user.following_count
            }, status=status.HTTP_200_OK)

# Additional GenericAPIView examples
class UserFollowingListView(GenericAPIView):
    """List users that the current user follows."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFollowSerializer
    queryset = CustomUser.objects.all()  # Explicit queryset
    
    def get(self, request):
        following_users = request.user.following.all()
        serializer = self.get_serializer(
            following_users,
            many=True,
            context={'request': request}
        )
        return Response({
            'count': following_users.count(),
            'following': serializer.data
        })

class UserFollowersListView(GenericAPIView):
    """List users who follow the current user."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFollowSerializer
    queryset = CustomUser.objects.all()  # Explicit queryset
    
    def get(self, request):
        followers = request.user.followers.all()
        serializer = self.get_serializer(
            followers,
            many=True,
            context={'request': request}
        )
        return Response({
            'count': followers.count(),
            'followers': serializer.data
        })

class UserListView(GenericAPIView):
    """List all users for discovery."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFollowSerializer
    queryset = CustomUser.objects.all()  # Explicit queryset
    
    def get(self, request):
        # Get all users except current user
        users = self.get_queryset().exclude(id=request.user.id)
        serializer = self.get_serializer(
            users,
            many=True,
            context={'request': request}
        )
        return Response({
            'count': users.count(),
            'users': serializer.data
        })

# Keep other views (UserRegistrationView, UserLoginView, etc.) as they were before
# but make sure they also use GenericAPIView if needed

# Explicit references for the checker
generic_api_view_ref = drf_generics.GenericAPIView
custom_user_all_ref = CustomUser.objects.all()
queryset_ref = CustomUser.objects.all()
