from django.db import models

"""
Author Model
------------
Represents a writer who can have multiple books.
Only contains one field: name.
The relationship: One Author → Many Books (via ForeignKey)
"""
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


"""
Book Model
----------
Represents a book written by an Author.
Fields:
- title: the book's name
- publication_year: year published
- author: foreign key linking book to its author
This establishes a one-to-many relationship.
"""
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

