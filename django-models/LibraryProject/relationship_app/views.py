#!/usr/bin/env python3
from django.shortcuts import render
from django.views.generic import DetailView   # ✅ For class-based view
from .models import Book, Library              # ✅ Must include Library model

# ✅ Function-based view — list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view — show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

