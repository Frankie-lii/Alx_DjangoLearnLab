from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    LikeSerializer
)
from .permissions import IsOwnerOrReadOnly
from .pagination import CustomPagination

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing posts."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'like_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like or unlike a post."""
        post = self.get_object()
        serializer = LikeSerializer(data=request.data)

        if serializer.is_valid():
            action_type = serializer.validated_data['action']

            if action_type == 'like':
                if post.likes.filter(id=request.user.id).exists():
                    return Response(
                        {'detail': 'You already liked this post.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                post.likes.add(request.user)
                return Response({'detail': 'Post liked successfully.'})
            else:  # unlike
                if not post.likes.filter(id=request.user.id).exists():
                    return Response(
                        {'detail': 'You have not liked this post.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                post.likes.remove(request.user)
                return Response({'detail': 'Post unliked successfully.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post."""
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)

        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """Get posts from users that the current user follows."""
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing comments."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
