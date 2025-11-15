from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import SearchForm, BookForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def book_list(request):
    form = SearchForm(request.GET or None)

    books = Book.objects.all()

    # Secure search (no SQL injection)
    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            books = books.filter(title__icontains=query)

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})


@csrf_protect
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BookForm()

    return render(request, "bookshelf/form_example.html", {"form": form})

# Documentation:
# - Django ORM prevents SQL injection
# - CSRF protection applied using @csrf_protect
# - User input validated using Django Forms

