from django.contrib.auth import login, authenticate
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import PermissionDenied
from django.forms import Form, ValidationError
from django.forms.utils import ErrorDict
from django.http import HttpRequest
import logging

from food_delivery_app.settings import DJANGO_ERROR_LOGGER


class LoginService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(DJANGO_ERROR_LOGGER)

    def login(self, request: HttpRequest, form: Form) -> None:
        if not form.is_valid():
            self.log_errors(form.errors)
            raise ValidationError("Certain fields are invalid")

        user: AbstractBaseUser | None = self.get_authenticated_user(
            request=request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        if not user:
            form.add_error(None, "Please type in the valid credentials")
            raise PermissionDenied

        self.handle_login(request, user)

    def log_errors(self, errors: ErrorDict) -> None:
        errors_data = errors.as_data()

        for key, error in list(errors_data.items()):
            self.logger.error(error[0].message)

    def get_authenticated_user(
        self, request: HttpRequest, username: str, password: str
    ) -> AbstractBaseUser | None:
        return authenticate(
            request,
            username=username,
            password=password,
        )

    def handle_login(self, request: HttpRequest, user: AbstractBaseUser) -> None:
        login(request, user)
