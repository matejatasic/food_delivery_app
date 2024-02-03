from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser
from django.forms import Form, EmailField, CharField, ImageField, PasswordInput
from django.urls import reverse_lazy

from django_select2.forms import HeavySelect2Widget  # type: ignore


class RegisterForm(UserCreationForm):
    email = EmailField(required=True)
    address = CharField(
        max_length=500,
        help_text="Type the whole address. The address should minimally hold street name and number, city and country. Eg. Street 123, City, Country",
        required=True,
    )
    image = ImageField(label="Profile Image", required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["address"].widget = HeavySelect2Widget(
            data_url=reverse_lazy("address")
        )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(Form):
    username = CharField(
        max_length=AbstractUser._meta.get_field("username").max_length,
        error_messages={
            "max_length": f"Username cannot be longer than {AbstractUser._meta.get_field('username').max_length}"
        },
    )
    password = CharField(
        max_length=AbstractBaseUser._meta.get_field("password").max_length,
        widget=PasswordInput,
        error_messages={
            "max_length": f"Password cannot be longer than {AbstractBaseUser._meta.get_field('password').max_length}"
        },
    )
