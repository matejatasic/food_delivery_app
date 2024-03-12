from django.contrib.auth.models import User


class UserService:
    def create(
        self,
        username: str,
        password: str,
        first_name: str | None,
        last_name: str | None,
        email: str,
    ) -> User:
        user = self.get_model_instance(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.full_clean()
        user.save()

        return user

    def get_model_instance(
        self, username: str, first_name: str | None, last_name: str | None, email: str
    ) -> User:
        return User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
