from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPITests(APITestCase):

    # ----------------------
    # Helper setup
    # ----------------------
    def setUp(self):
        self.client = APIClient()

        # Create a user for authenticated tests
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create initial Author and Book
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )

        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])

    # ----------------------
    # Read Tests (No Auth Required)
    # ----------------------
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    # ----------------------
    # Create (Requires Authentication)
    # ----------------------
    def test_create_book_requires_auth(self):
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id,
        }

        # Not authenticated → should fail
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password123")

        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id,
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    # ----------------------
    # Update Tests
    # ----------------------
    def test_update_book_requires_auth(self):
        data = {"title": "Updated Book"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")

        data = {
            "title": "Updated Book",
            "publication_year": 2020,
            "author": self.author.id
        }

        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    # ----------------------
    # Delete Tests
    # ----------------------
    def test_delete_requires_auth(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_authenticated(self):
        self.client.login(username="testuser", password="password123")

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    # ----------------------
    # Filtering Tests
    # ----------------------
    def test_filter_by_title(self):
        response = self.client.get(self.list_url + "?title=Test Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test Book")

    def test_filter_by_publication_year(self):
        response = self.client.get(self.list_url + "?publication_year=2020")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    # ----------------------
    # Search Tests
    # ----------------------
    def test_search_book(self):
        response = self.client.get(self.list_url + "?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    # ----------------------
    # Ordering Tests
    # ----------------------
    def test_order_books(self):
        response = self.client.get(self.list_url + "?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

