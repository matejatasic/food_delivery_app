from django.test import TestCase
from django.urls import reverse
from faker import Faker  # type: ignore
from http import HTTPStatus
from json import dumps


class LogoutTests(TestCase):
    logout_url: str = reverse("logout")
    login_url: str = reverse("login")
    registration_url: str = reverse("register")
    home_url: str = reverse("home")

    def test_logout_successful(self) -> None:
        """Asserts the user is successfully logged out"""

        self.faker = Faker()
        fake_address = self.faker.address()
        register_payload: dict[str, str] = {
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
        """Asserts the user cannot log out if he is not logged in"""

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(self.login_url, response["location"])
