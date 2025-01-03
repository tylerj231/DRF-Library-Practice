from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book


class TestUnAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_allow_list_books(self):
        url = reverse("books:book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_forbid_create_book(self):
        url = reverse("books:book-list")
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 50,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test1234"
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_allow_list_books(self):
        url = reverse("books:book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_forbid_create_book(self):
        url = reverse("books:book-list")
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 50,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_retrieve_book(self):
        book = Book.objects.create(
            title="Test title",
            author="Test author",
            cover="Hard",
            inventory=50,
        )
        url = reverse("books:book-detail", args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_admin_allow_list_books(self):
        url = reverse("books:book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_allow_create_book(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse("books:book-list")
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 50,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_allow_delete_book(self):
        self.user.is_staff = True
        self.user.save()
        book = Book.objects.create(
            title="Test title",
            author="Test author",
            cover="Hard",
            inventory=50,
        )
        url = reverse("books:book-detail", args=[book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
