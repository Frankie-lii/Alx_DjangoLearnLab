# LibraryProject/bookshelf/views.py

from django.shortcuts import render
from .forms import ExampleForm  # <-- Make sure this line exists

def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # process data here
            pass
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

