from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/auth/register/"
        self.login_url = "/auth/login/"
        self.valid_user_data = {
            "name": "John Doe",
            "phone": "+919876543210",
            "password": "securepassword",
            "role": "user",
        }
        self.invalid_phone_data = {
            "name": "John Doe",
            "phone": "invalid_phone",
            "password": "securepassword",
            "role": "user",
        }
        self.invalid_login_data = {
            "phone": "+919876543210",
            "password": "wrongpassword",
        }

    def test_register_user_success(
        self,
    ):

        # Perform the registration request
        response = self.client.post(self.register_url, self.valid_user_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Registration successful.")
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["name"], self.valid_user_data["name"])
        self.assertEqual(response.data["user"]["role"], self.valid_user_data["role"])

    
    def test_login_user_success(self):

        # Create a user for login
        User.objects.create_user(
            phone=self.valid_user_data["phone"],
            password=self.valid_user_data["password"],
            name=self.valid_user_data["name"],
            role=self.valid_user_data["role"],
        )

        login_data = {
            "phone": self.valid_user_data["phone"],
            "password": self.valid_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Login successful.")
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["phone"], self.valid_user_data["phone"])
        self.assertEqual(response.data["user"]["role"], self.valid_user_data["role"])
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertTrue(len(response.data["access"]) > 0)
        self.assertTrue(len(response.data["refresh"]) > 0)

    def test_login_user_invalid_credentials(self):

        User.objects.create_user(
            phone=self.valid_user_data["phone"],
            password=self.valid_user_data["password"],
            name=self.valid_user_data["name"],
            role=self.valid_user_data["role"],
        )
        response = self.client.post(self.login_url, self.invalid_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0], "Invalid phone or password."
        )

    def test_login_user_invalid_phone_format(self):
        response = self.client.post(self.login_url, self.invalid_phone_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn(
            "Invalid phone or password.", response.data["non_field_errors"][0]
        )
