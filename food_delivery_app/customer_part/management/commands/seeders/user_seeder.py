from django.contrib.auth.models import User, Group
from sys import stdout

from .base_seeder import BaseSeeder


class UserSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the user data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting User instances")
        User.objects.all().delete()

    def create_records(self) -> None:
        print("Creating user")

        data = [
            {
                "username": "alaya",
                "first_name": "Alaya",
                "last_name": "Heath",
                "password": "password",
                "email": "alaya@test.com",
                "group": "Customer",
            },
            {
                "username": "kashton",
                "first_name": "Kashton",
                "last_name": "Krueger",
                "password": "password",
                "email": "kashton@test.com",
                "group": "Customer",
            },
            {
                "username": "jamir",
                "first_name": "Jamir",
                "last_name": "Meyers",
                "password": "password",
                "email": "jamir@test.com",
                "group": "Customer",
            },
            {
                "username": "mark",
                "first_name": "Mark",
                "last_name": "Travis",
                "password": "password",
                "email": "mark@test.com",
                "group": "Driver",
            },
        ]

        for user_data in data:
            user = User(
                username=user_data["username"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
            )
            user.set_password(user_data["password"])
            user.save()
            Group.objects.get(name=user_data["group"]).user_set.add(user)

            print(f"User {user} created.")
