from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm, ValidationError
from django.http import HttpRequest
from json import loads

from ..exceptions import AddressValidationError
from ..forms import LoginForm
from .login_service import LoginService
from .profile_service import ProfileService
from .user_service import UserService


class RegisterService:
    def register(self, request: HttpRequest, form: ModelForm) -> None:
        if not form.is_valid():
            raise ValidationError("Certain fields are invalid")

        try:
            user: User = self.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data.get("first_name", None),
                last_name=form.cleaned_data.get("last_name", None),
                email=form.cleaned_data["email"],
                address=loads(form.cleaned_data["address"])[0]["fields"],
            )
        except AddressValidationError:
            form.add_error(None, "There was a problem while validating the adddress")

            raise ValidationError("There was a problem while validating the adddress")

        self.create_profile(user, form.cleaned_data.get("image", None))

        self.login_user(
            request=request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

    def create_user(
        self,
        username: str,
        password: str,
        first_name: str | None,
        last_name: str | None,
        email: str,
        address: dict[str, str],
    ) -> User:
        user_service: UserService = self.get_user_service()

        return user_service.create(
            username,
            password,
            first_name,
            last_name,
            email,
            address,
        )

    def get_user_service(self) -> UserService:
        return UserService()

    def create_profile(self, user: User, image: InMemoryUploadedFile | None) -> None:
        profile_service: ProfileService = self.get_profile_service()

        profile_service.create(user, image)

    def get_profile_service(self) -> ProfileService:
        return ProfileService()

    def login_user(self, request: HttpRequest, username: str, password: str) -> None:
        login_service = self.get_login_service()
        login_form = LoginForm(
            {
                "username": username,
                "password": password,
            }
        )

        login_service.login(request, login_form)

    def get_login_service(self) -> LoginService:
        return LoginService()
