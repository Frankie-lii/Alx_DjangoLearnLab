from django_filters import rest_framework
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ✔ Filtering, Searching, Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # ✔ Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # ✔ Search fields (partial text search)
    search_fields = ['title', 'author__name']

    # ✔ Ordering fields
    ordering_fields = ['title', 'publication_year']

    # ✔ Default ordering
    ordering = ['title']

