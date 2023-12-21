from django.contrib.auth.models import User
from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse
from faker import Faker  # type: ignore
from http import HTTPStatus
from json import dumps


class LoginTests(TestCase):
    login_url: str = reverse("login")
    registration_url: str = reverse("register")
    logout_url: str = reverse("logout")
    home_url: str = reverse("home")

    def setUp(self) -> None:
        self.faker = Faker()
        fake_address = self.faker.address()
        self.register_payload: dict[str, str] = {
            "username": "user",
            "password1": "p@ssword123",
            "password2": "p@ssword123",
            "email": "user@test.com",
            "address": dumps(
                [
                    {
                        "fields": {
                            "latitude": float(self.faker.latitude()),
                            "longitude": float(self.faker.longitude()),
                            "raw": fake_address,
                            "address_line": fake_address,
                            "district_1": self.faker.country_code(),
                            "district_2": self.faker.country_code(),
                            "country": self.faker.country(),
                            "locality": self.faker.city(),
                            "postal_code": self.faker.postcode(),
                        }
                    }
                ]
            ),
        }
        self.login_payload: dict[str, str] = {
            "username": self.register_payload["username"],
            "password": self.register_payload["password1"],
        }

    def test_access_to_login_as_authenticated_user_unsuccessful(self):
        """Asserts that the authenticated user cannot land on the login page"""

        self.client.post(self.registration_url, self.register_payload)
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)

    def test_login_successful_with_valid_user(self) -> None:
        """Asserts user is logged in if the credentials are valid"""

        self.client.post(self.registration_url, self.register_payload)
        self.client.post(self.logout_url)
        response = self.client.post(self.login_url, self.login_payload)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["location"], self.home_url)
        self.assertTrue(
            User.objects.get(username=self.login_payload["username"]).is_authenticated
        )

    def test_login_with_invalid_input_returns_errors(self) -> None:
        """Asserts the server returns errors if the credentials are not valid"""

        response = self.client.post(self.login_url, self.login_payload)

        form_errors: dict[str, list[ValidationError]] = response.context[
            "form"
        ].errors.as_data()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(form_errors), 1)
