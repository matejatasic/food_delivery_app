from django.test import TestCase
from faker import Faker  # type: ignore

from ...forms import RegisterForm


class RegisterFormTests(TestCase):
    register_form: RegisterForm
    faker = Faker()

    def setUp(self):
        self.register_form = None

    def test_register_form_valid_when_input_is_valid(self):
        """Asserts that the register form is valid, with no errors, when the input is valid"""

        password = self.faker.password()
        data = {
            "username": self.faker.profile(fields=["username"])["username"],
            "email": self.faker.email(),
            "password1": password,
            "password2": password,
            "address": self.faker.address(),
        }
        self.register_form = RegisterForm(data=data)

        self.assertTrue(self.register_form.is_valid())
        self.assertEqual(len(self.register_form.errors), 0)

    def test_register_form_not_valid_when_no_input_given(self):
        """Asserts that the register form is not valid when no input is given"""

        self.register_form = RegisterForm(data={})

        required_fields = [
            field for key, field in RegisterForm.base_fields.items() if field.required
        ]

        self.assertFalse(self.register_form.is_valid())
        self.assertEqual(len(self.register_form.errors), len(required_fields))

    def test_register_form_invalid_when_email_invalid(self):
        """Asserts that the register form is not valid when email is not valid"""

        password = self.faker.password()
        data = {
            "username": self.faker.profile(fields=["username"])["username"],
            "email": "invalid email",
            "password1": password,
            "password2": password,
            "address": self.faker.address(),
        }
        self.register_form = RegisterForm(data=data)

        self.assertFalse(self.register_form.is_valid())
        self.assertEqual(len(self.register_form.errors), 1)

    def test_register_invalid_when_image_invalid(self):
        """Asserts that the register form is not valid when image is not valid"""

        password = self.faker.password()
        data = {
            "username": self.faker.profile(fields=["username"])["username"],
            "email": self.faker.email(),
            "password1": password,
            "password2": password,
            "address": self.faker.address(),
        }
        self.register_form = RegisterForm(data, {"image": "invalid image"})

        self.assertFalse(self.register_form.is_valid())
        self.assertEqual(len(self.register_form.errors), 1)
