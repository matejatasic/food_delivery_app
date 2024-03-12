from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch, Mock

from ..factories import UserServiceCreateParametersFactory
from ...services.user_service import UserService


class UserServiceTests(TestCase):
    user_service = UserService()

    @patch.object(UserService, "get_model_instance")
    def test_create_returns_user_model_instance_when_created_successfully(
        self, get_model_instance_mock
    ):
        """Asserts that the method for creating a user returns a user if it is successfully creation"""

        user_mock = Mock(spec=User)
        get_model_instance_mock.return_value = user_mock
        user_mock.full_clean.return_value = None
        user_mock.save.return_value = None

        result = self.user_service.create(**UserServiceCreateParametersFactory())

        self.assertIsInstance(result, Mock)
