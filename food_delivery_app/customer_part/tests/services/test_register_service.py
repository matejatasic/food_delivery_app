from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import HttpRequest
from django.test import TestCase
from faker import Faker  # type: ignore
from json import dumps
from unittest.mock import patch, Mock

from ...exceptions import AddressValidationError
from ...services.register_service import RegisterService


class RegisterServiceTests(TestCase):
    register_service = RegisterService()
    faker = Faker()
    request_mock: Mock
    form_mock: Mock

    def setUp(self) -> None:
        self.request_mock = Mock(spec=HttpRequest)
        self.form_mock = Mock(spec=ModelForm)
        fake_address = self.faker.address()
        self.form_mock.cleaned_data = {
            "username": self.faker.profile(fields=["username"])["username"],
            "password1": self.faker.password(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "email": self.faker.email(),
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

    @patch.object(RegisterService, "login_user")
    @patch.object(RegisterService, "create_profile")
    @patch.object(RegisterService, "create_user")
    def test_register_successfully_when_no_errors_raised(
        self, create_user_mock, create_profile_mock, login_user_mock
    ):
        """Asserts that the registration is handled successfully, without any errors"""

        create_user_mock.return_value = Mock(spec=User)
        create_profile_mock.return_value = None
        login_user_mock.return_value = None

        self.register_service.register(self.request_mock, self.form_mock)

    def test_register_raises_the_validaiton_error_if_the_form_is_invalid(self):
        """Asserts that the registration raises the ValidationError if the form has received invalid input"""

        self.form_mock.is_valid.return_value = False

        self.assertRaises(
            ValidationError,
            self.register_service.register,
            *[self.request_mock, self.form_mock]
        )

    @patch.object(RegisterService, "create_user")
    def test_register_raises_address_validation_error_on_validation_error_raised(
        self, create_user_mock
    ):
        """Asserts that the registration raises an AddressValidationError if the ValidationError is raised"""

        create_user_mock.side_effect = AddressValidationError(
            {"some_field": "Invalid field"}
        )

        self.assertRaises(
            ValidationError,
            self.register_service.register,
            *[self.request_mock, self.form_mock]
        )
