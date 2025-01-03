import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing


class UnAuthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_list_borrowings_forbid(self):
        url = reverse("borrowings:borrowing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test",
            password="test1234",
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_list_borrowings_allow(self):
        url = reverse("borrowings:borrowing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_detail_borrowing_allow(self):
        user = self.user
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Hard",
            inventory=50,
        )
        borrowing = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
            book=book,
            user_id=user.id
        )
        url = reverse("borrowings:borrowing-detail", args=[borrowing.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_create_borrowing_allow(self):
        url = reverse("borrowings:borrowing-list")
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Hard",
            inventory=50,
        )
        payload = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today() + datetime.timedelta(days=1),
            "book": book.id,
            "user": self.user.id,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_borrowing_list_allow(self):
        self.user.is_staff = True
        self.user.save()
        url = reverse("borrowings:borrowing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_borrowing_detail_allow(self):
        self.user.is_staff = True
        self.user.save()
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Hard",
            inventory=50,
        )
        borrowing = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
            book=book,
            user_id=self.user.id
        )
        url = reverse("borrowings:borrowing-detail", args=[borrowing.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_admin_create_borrowing_allow(self):
        self.user.is_staff = True
        self.user.save()

        url = reverse("borrowings:borrowing-list")
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Soft",
            inventory=50,
        )
        payload = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today() + datetime.timedelta(days=2),
            "book": book.id,
            "user": self.user.id,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
