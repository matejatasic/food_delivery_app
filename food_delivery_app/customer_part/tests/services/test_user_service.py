from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from faker import Faker  # type: ignore
from unittest.mock import patch, Mock

from ...exceptions import AddressValidationError
from ...models import Address
from ...services.address_service import AddressService
from ...services.user_service import UserService


class UserServiceTests(TestCase):
    user_service = UserService()
    faker = Faker()

    @patch.object(UserService, "get_address_service")
    @patch.object(UserService, "get_model_instance")
    def test_create_returns_user_model_instance_when_created_successfully(
        self, get_model_instance_mock, get_address_service_mock
    ):
        """Asserts that the method for creating a user returns a user if it is successfully creation"""

        user_mock = Mock(spec=User)
        get_model_instance_mock.return_value = user_mock
        user_mock.full_clean.return_value = None
        user_mock.save.return_value = None

        address_service_mock = Mock(spec=AddressService)
        address_mock = Mock(spec=Address)
        get_address_service_mock.return_value = address_service_mock
        address_service_mock.create.return_value = address_mock

        fake_address = self.faker.address()
        address_dict = {
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

        result = self.user_service.create(
            username=self.faker.profile(fields=["username"])["username"],
            password=self.faker.password(),
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            email=self.faker.email(),
            address=address_dict,
        )

        self.assertIsInstance(result, Mock)

    @patch.object(UserService, "log_errors")
    @patch.object(UserService, "get_address_service")
    @patch.object(UserService, "get_model_instance")
    def test_create_raises_address_validation_error_on_validation_error_raised(
        self, get_model_instance_mock, get_address_service_mock, log_errors_mock
    ):
        """Asserts that the method for creating a user raises an AddressValidationError if the ValidationError is raised"""

        log_errors_mock.return_value = None
        user_mock = Mock(spec=User)
        get_model_instance_mock.return_value = user_mock
        user_mock.full_clean.return_value = None
        user_mock.save.return_value = None

        address_service_mock = Mock(spec=AddressService)
        get_address_service_mock.return_value = address_service_mock
        address_service_mock.create.side_effect = ValidationError(
            {"some_field": "Invalid field"}
        )

        fake_address = self.faker.address()
        address_dict = {
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
        result = [
            self.faker.profile(fields=["username"])["username"],
            self.faker.password(),
            self.faker.first_name(),
            self.faker.last_name(),
            self.faker.email(),
            address_dict,
        ]

        self.assertRaises(
            AddressValidationError,
            self.user_service.create,
            *result,
        )
