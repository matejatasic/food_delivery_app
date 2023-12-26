from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from unittest.mock import patch, Mock

from ...exceptions import AddressValidationError
from ..factories import UserServiceCreateParametersFactory
from ...models import Address
from ...services.address_service import AddressService
from ...services.user_service import UserService


class UserServiceTests(TestCase):
    user_service = UserService()

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

        result = self.user_service.create(**UserServiceCreateParametersFactory())

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

        self.assertRaises(
            AddressValidationError,
            self.user_service.create,
            **UserServiceCreateParametersFactory(),
        )
