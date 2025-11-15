from django import forms
from .models import Book

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "Search books..."})
    )

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description"]

# Forms automatically prevent SQL injection through Django ORM.

