from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class LogoutTests(TestCase):
    logout_url: str = reverse("logout")
    login_url: str = reverse("login")
    registration_url: str = reverse("register")
    home_url: str = reverse("home")

    def test_logout_successful(self) -> None:
        register_payload: dict[str, str] = {
            "username": "user",
            "password1": "p@ssword123",
            "password2": "p@ssword123",
            "email": "user@test.com",
            "address": "Some address",
        }
        login_payload: dict[str, str] = {
            "username": register_payload["username"],
            "password": register_payload["password1"],
        }

        self.client.post(self.registration_url, register_payload)
        self.client.post(self.login_url, login_payload)
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)

    def test_logout_unsuccessful_when_user_anonymous(self) -> None:
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(self.login_url, response["location"])
