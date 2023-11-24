from django.contrib.auth import login, authenticate
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import PermissionDenied
from django.forms import Form, ValidationError
from django.http import HttpRequest


class LoginService:
    def login(self, request: HttpRequest, form: Form) -> None:
        if not form.is_valid():
            raise ValidationError("Certain fields are invalid")

        user: AbstractBaseUser | None = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        if not user:
            form.add_error(None, "Please type in the valid credentials")
            raise PermissionDenied

        login(request, user)
