from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

"""
BookSerializer
--------------
Serializes all fields from Book model.
Includes custom validation to ensure the publication year is not in the future.
"""
class BookSerializer(serializers.ModelSerializer):

    # Custom validation (publication year must NOT be in the future)
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


"""
AuthorSerializer
----------------
Serializes the author model with:
- name field
- nested list of books (using BookSerializer)
Uses the related_name='books' from the Book model.
"""
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

