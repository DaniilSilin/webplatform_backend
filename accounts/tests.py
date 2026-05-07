from unittest import TestCase
from rest_framework.exceptions import ValidationError
from .validators import validate_username, check_password_complexity
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class RegistrationAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_registration_with_common_password_fails(self):
        data = {
            "email": "test@test.com",
            "username": "tester_next",
            "password": "Password123!",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserValidatorsTest(TestCase):

    def test_username_too_short(self):
        with self.assertRaises(ValidationError):
            validate_username("al")

    def test_username_valid(self):
        username = "alex_dev"
        self.assertEqual(validate_username(username), username)

    def test_password_complexity_no_special_char(self):
        with self.assertRaises(ValidationError):
            check_password_complexity("StrongPass123", "someuser")

    def test_password_is_common(self):
        with self.assertRaises(ValidationError):
            check_password_complexity("qwerty", "someuser")
