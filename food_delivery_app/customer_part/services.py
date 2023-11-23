from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Profile


class RegisterService:
    def register(self, form: ModelForm) -> None:
        if not form.is_valid():
            raise ValidationError("Certain fields are invalid")

        user_service = UserService()
        user = user_service.create(
            form.cleaned_data["username"],
            form.cleaned_data["password1"],
            form.cleaned_data["first_name"],
            form.cleaned_data["last_name"],
            form.cleaned_data["email"],
        )

        profile_service = ProfileService()
        profile_service.create(user, form.cleaned_data["image"])


class UserService:
    def create(
        self,
        username: str,
        password: str,
        first_name: str | None,
        last_name: str,
        email: str,
    ) -> User:
        user = User(
            username=username, first_name=first_name, last_name=last_name, email=email
        )
        user.set_password(password)
        user.full_clean()
        user.save()

        return user


class ProfileService:
    def create(self, user: User, image: InMemoryUploadedFile) -> Profile:
        profile = Profile(user=user, image=image)
        profile.full_clean()
        profile.save()

        return profile
