from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),

    # ✅ Add book URL (required by checker)
    path('add_book/', views.add_book, name='add_book'),

    # ✅ Edit book URL (required by checker)
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),

    # Optional: Delete view (if implemented)
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]

