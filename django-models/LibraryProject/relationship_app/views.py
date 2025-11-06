#!/usr/bin/env python3
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# ✅ Function-based view: lists all books
def list_books(request):
    books = Book.objects.all()
    # Checker expects "relationship_app/list_books.html"
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view: shows details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

