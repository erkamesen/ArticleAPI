"""
Tests for User API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


LOGIN_URL = reverse("auth:knox-login")
LOGOUT_URL = reverse("auth:knox-logout")
LOGOUTALL_URL = reverse("auth:knox-logoutall")
REGISTER_URL = reverse("auth:knox-register")


def create_user(username="testUser",
                email="test@mail.com",
                password="testPass123"):
    return get_user_model().objects.create_user(username, email, password)


class UserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_succesfully(self):
        """Test register with valid credentials"""
        payload = {
            "username": "testuser",
            "email": "test123@mail.com",
            "password": "testpass123"
        }

        res = self.client.post(REGISTER_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)
        self.assertNotIn("password", res.data)
        self.assertEqual(payload["username"], res.data.get("user")["username"])

    def test_register_failure(self):
        """Test register with invalid credentials"""
        payload = {
            "email": "test123@mail.com",
            "password": "testpass123"
        }

        res = self.client.post(REGISTER_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", res.data)

    def test_register_exist_email(self):
        """Test register exist email and raise error"""
        create_user(email="exist@mail.com")

        payload = {
            "username": "testuser",
            "email": "exist@mail.com",
            "password": "testpass123"
        }

        res = self.client.post(REGISTER_URL, data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)

    def test_register_exist_username(self):
        """Test register exist email and raise error"""
        create_user(username="testuser")

        payload = {
            "username": "testuser",
            "email": "test123@mail.com",
            "password": "testpass123"
        }

        res = self.client.post(REGISTER_URL, data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", res.data)

    def test_register_short_password(self):
        """Test register short password and raise an error"""
        payload = {
            "username": "testuser",
            "email": "test123@mail.com",
            "password": "123"
        }

        res = self.client.post(REGISTER_URL, data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)

    def test_login_succesfully(self):
        """Test login succesfully"""
        create_user(username="testuser",
                    email="test123@mail.com",
                    password="testpass123",
                    )

        payload = {
            "username": "testuser",
            "password": "testpass123"
        }

        res = self.client.post(LOGIN_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)
        self.assertIn("expiry", res.data)

    def test_login_unsuccesfully(self):
        """Test login unsuccesfully"""

        payload = {
            "username": "nonexistuser",
            "password": "testpass123",
        }

        res = self.client.post(LOGIN_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", res.data)

    def test_logout_succesfully(self):
        """Test logout after login with succesfully"""
        create_user(username="testuser",
                    email="test123@mail.com",
                    password="testpass123",
                    )
        # LOGIN

        payload = {
            "username": "testuser",
            "password": "testpass123"
        }

        res = self.client.post(LOGIN_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

        token = res.data.get("token")

        # LOGOUT
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_logoutall_succesfully(self):
        """Test logout after login with succesfully"""
        create_user(username="testuser",
                    email="test123@mail.com",
                    password="testpass123",
                    )
        # LOGIN

        payload = {
            "username": "testuser",
            "password": "testpass123"
        }

        res = self.client.post(LOGIN_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

        token = res.data.get("token")

        # LOGOUT
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        res = self.client.post(LOGOUTALL_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
