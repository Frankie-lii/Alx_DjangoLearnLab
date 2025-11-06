from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []


# 2️⃣ List all books in a specific library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []


# 3️⃣ Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# 🔍 Sample test outputs
if __name__ == "__main__":
    print("Books by J.K. Rowling:")
    for book in get_books_by_author("J.K. Rowling"):
        print(f" - {book.title}")

    print("\nBooks in Central Library:")
    for book in get_books_in_library("Central Library"):
        print(f" - {book.title}")

    print("\nLibrarian of Central Library:")
    librarian = get_librarian_for_library("Central Library")
    print(librarian.name if librarian else "No librarian found")

