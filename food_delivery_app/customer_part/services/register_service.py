from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError
from django.http import HttpRequest

from ..forms import LoginForm
from .login_service import LoginService
from .profile_service import ProfileService
from .user_service import UserService


class RegisterService:
    def register(self, request: HttpRequest, form: ModelForm) -> None:
        if not form.is_valid():
            raise ValidationError("Certain fields are invalid")

        user_service: UserService = UserService()
        user: User = user_service.create(
            form.cleaned_data["username"],
            form.cleaned_data["password1"],
            form.cleaned_data["first_name"],
            form.cleaned_data["last_name"],
            form.cleaned_data["email"],
        )

        profile_service: ProfileService = ProfileService()
        profile_service.create(user, form.cleaned_data["image"])

        login_service = LoginService()
        login_form = LoginForm(
            {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password1"],
            }
        )
        login_service.login(request, login_form)
