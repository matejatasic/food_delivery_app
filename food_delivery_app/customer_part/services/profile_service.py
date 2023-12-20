from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..models import Profile


class ProfileService:
    def create(self, user: User, image: InMemoryUploadedFile | None) -> Profile:
        profile = self.get_model_instance(user=user, image=image)
        profile.full_clean()
        profile.save()

        return profile

    def get_model_instance(
        self, user: User, image: InMemoryUploadedFile | None
    ) -> Profile:
        return Profile(user=user, image=image)
