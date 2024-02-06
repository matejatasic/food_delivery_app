from django.test import TestCase

from ..factories import LoginFormDataFactory
from ...forms import LoginForm


class LoginFormTests(TestCase):
    login_form: LoginForm

    def setUp(self):
        self.register_form = None

    def test_login_form_valid_when_input_is_valid(self):
        """Asserts that the login form is valid, with no errors, when the input is valid"""

        data = LoginFormDataFactory()
        self.login_form = LoginForm(data=data)

        self.assertTrue(self.login_form.is_valid())
        self.assertEqual(len(self.login_form.errors), 0)

    def test_login_form_not_valid_when_no_input_given(self):
        """Asserts that the login form is not valid when no input is given"""

        self.login_form = LoginForm(data={})

        self.assertFalse(self.login_form.is_valid())
        self.assertEqual(len(self.login_form.errors), len(LoginForm.base_fields))

    def test_login_form_not_valid_when_input_is_longer_than_max_length(self):
        """Asserts that the login form is not valid if the input fields have bigger length than the allowed one"""

        data = LoginFormDataFactory(is_invalid_input=True)
        self.login_form = LoginForm(data=data)

        self.assertFalse(self.login_form.is_valid())
        self.assertEqual(len(self.login_form.errors), len(data.keys()))
