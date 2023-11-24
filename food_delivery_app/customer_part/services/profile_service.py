from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..models import Profile


class ProfileService:
    def create(self, user: User, image: InMemoryUploadedFile) -> Profile:
        profile = Profile(user=user, image=image)
        profile.full_clean()
        profile.save()

        return profile
