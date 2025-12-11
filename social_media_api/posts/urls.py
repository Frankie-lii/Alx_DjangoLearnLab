from django.urls import path
from .views import FeedAPIView

urlpatterns = [
    path('feed/', FeedAPIView.as_view(), name='feed'),
]
