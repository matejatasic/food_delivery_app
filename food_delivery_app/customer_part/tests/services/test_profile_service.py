from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from unittest.mock import patch, Mock

from ...exceptions import AddressValidationError
from ..factories import AddressFieldsFactory, ProfileServiceCreateParametersFactory
from ...models import Profile
from ...services.address_service import AddressService
from ...services.profile_service import ProfileService


class ProfileServiceTests(TestCase):
    profile_service = ProfileService()
    query = "Some Address"

    @patch.object(ProfileService, "get_model_instance")
    def test_create_returns_profile_model_instance_when_created_successfully(
        self, get_model_instance_mock
    ):
        """Asserts that the method for creating a profile returns a profile if it is successfully creation"""

        user_mock = Mock(spec=User)
        image_mock = Mock(spec=InMemoryUploadedFile)
        address = AddressFieldsFactory()

        get_model_instance_mock.return_value = Mock(spec=Profile)

        result = self.profile_service.create(
            user=user_mock, image=image_mock, address=address
        )

        self.assertIsInstance(result, Mock)

    @patch.object(ProfileService, "log_errors")
    @patch.object(ProfileService, "get_address_service")
    @patch.object(ProfileService, "get_model_instance")
    def test_create_raises_address_validation_error_on_validation_error_raised(
        self, get_model_instance_mock, get_address_service_mock, log_errors_mock
    ):
        """Asserts that the method for creating a profile raises an AddressValidationError if the ValidationError is raised"""

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
            self.profile_service.create,
            **ProfileServiceCreateParametersFactory(),
        )
