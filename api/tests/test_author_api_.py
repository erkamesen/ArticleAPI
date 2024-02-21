"""
Tests for Author API
"""

from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from api.models import Author
from rest_framework import status


LIST_POST_URL = reverse("api:authors-list")


def create_author(name="testname", surname="testsurname",
                  email="test@example.com", phone="123123123"):
    author = Author.objects.create(name=name, surname=surname,
                                   email=email, phone=phone)
    return author


def create_authors(lim=5):
    authors = [Author(name=f"testname{i}",
                      surname=f"testsurname{i}",
                      email=f"test{i}@example.com",
                      phone=f"123123123{i}") for i in range(1, lim + 1)]
    Author.objects.bulk_create(authors)


def detail_url(author_id):
    return reverse("api:authors-detail", args=[author_id,])


class AuthorTests(TestCase):
    """Tests for Author model"""

    def setUp(self):
        self.client = APIClient()

    def test_list_authors(self):
        """Test for list all authors in database"""
        create_authors(3)

        res = self.client.get(LIST_POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_create_author_with_correct_credentials(self):  # Positive
        """Test create author succesfully"""
        payload = {
            "name": "Test-Name",
            "surname": "Test-Surname",
            "email": "test@mail.com",
            "phone": "123123123",
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("name"), payload.get("name"))

    def test_create_author_with_wrong_credentials(self):  # Negative
        """Test create author and get 400 status code"""
        payload = {  # There is no name
            "surname": "Test-Surname",
            "email": "test",  # wrong email
            "phone": "123123123",
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", res.data)
        self.assertIn("email", res.data)

        self.assertNotIn("surname", res.data)
        self.assertNotIn("phone", res.data)

    def test_get_author_detail(self):
        """Test retrieve spesific author details"""
        author = create_author()
        url = detail_url(author.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), author.name)
        self.assertEqual(res.data.get("surname"), author.surname)
        self.assertEqual(res.data.get("email"), author.email)
        self.assertEqual(res.data.get("phone"), author.phone)

    def test_put_author_succesfully(self):  # Positive
        """Test put method in author infos"""
        author = create_author()
        url = detail_url(author.id)

        payload = {
            "name": "New Name",
            "surname": "New Surname",
            "email": "newtest@mail.com",
            "phone": "123123123"
        }

        res = self.client.put(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_author_failure(self):  # Negative
        """Test put method in author infos"""
        author = create_author()
        url = detail_url(author.id)

        payload = {
            "name": "New Name",
            "surname": "New Surname",
            "email": "newtest@mail.com",
        }

        res = self.client.put(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_author_succesfully(self):
        """Test patch method in author infos"""

        author = create_author()
        url = detail_url(author.id)

        payload = {
            "name": "New Name",
        }

        res = self.client.patch(url, data=payload)

        author.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), author.name)

    def test_author_email_must_be_unique(self):
        """Test for create author with exists email and get error"""
        create_author(email="exist@mail.com")

        payload = {
            "name": "Test",
            "surname": "Test",
            "email": "exist@mail.com",
            "phone": "123123123"
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)

    def test_delete_author(self):
        """Test delete post api"""
        author = create_author()
        url = detail_url(author.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
