from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from .profile_service import ProfileService
from .user_service import UserService


class RegisterService:
    def register(self, form: ModelForm) -> None:
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
