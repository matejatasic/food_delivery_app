from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError, PermissionDenied
from django.forms import Form
from django.http import HttpRequest
from django.test import TestCase
from unittest.mock import patch, Mock

from ..factories import LoginFormDataFactory
from ...services.login_service import LoginService


class LoginServiceTests(TestCase):
    login_service = LoginService()
    request_mock: Mock
    form_mock: Mock

    def setUp(self) -> None:
        self.request_mock = Mock(spec=HttpRequest)
        self.form_mock = Mock(spec=Form)
        self.form_mock.cleaned_data = LoginFormDataFactory()

    @patch.object(LoginService, "handle_login")
    @patch.object(LoginService, "get_authenticated_user")
    def test_login_successfully_when_no_errors_raised(
        self, get_authenticated_user_mock, handle_login_mock
    ):
        """Asserts that the login is handled successfully, without any errors"""

        get_authenticated_user_mock.return_value = Mock(spec=AbstractBaseUser)
        handle_login_mock.return_value = None

        self.login_service.login(self.request_mock, self.form_mock)

    @patch.object(LoginService, "log_errors")
    def test_login_raises_the_validaiton_error_if_the_form_is_invalid(
        self, log_errors_mock
    ):
        """Asserts that the login raises the ValidationError if the form has received invalid input"""

        self.form_mock.is_valid.return_value = False
        log_errors_mock.return_value = None

        self.assertRaises(
            ValidationError,
            self.login_service.login,
            *[self.request_mock, self.form_mock]
        )

    @patch.object(LoginService, "get_authenticated_user")
    def test_login_raises_the_permission_denied_error_if_the_user_cant_be_authenticated(
        self, get_authenticated_user_mock
    ):
        """Asserts that the login raises the PermissionDenied error if the invalid credentials are passed"""

        get_authenticated_user_mock.return_value = None

        self.assertRaises(
            PermissionDenied,
            self.login_service.login,
            *[self.request_mock, self.form_mock]
        )
