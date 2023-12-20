from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from faker import Faker  # type: ignore
from unittest.mock import patch, Mock

from ...models import Profile
from ...services.profile_service import ProfileService


class ProfileServiceTests(TestCase):
    profile_service = ProfileService()
    query = "Some Address"
    faker = Faker()

    @patch.object(ProfileService, "get_model_instance")
    def test_create_returns_profile_model_instance_when_created_successfully(
        self, get_model_instance_mock
    ):
        """Asserts that the method for creating a profile returns a profile if it is successfully creation"""

        user_mock = Mock(spec=User)
        image_mock = Mock(spec=InMemoryUploadedFile)

        get_model_instance_mock.return_value = Mock(spec=Profile)

        result = self.profile_service.create(user=user_mock, image=image_mock)

        self.assertIsInstance(result, Mock)
