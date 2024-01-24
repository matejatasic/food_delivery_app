from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser

class UserModelBackend(ModelBackend):
    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        UserModel = get_user_model()
        try:
            return UserModel.objects.select_related("profile").get(pk=user_id)
        except UserModel.DoesNotExist:
            return None