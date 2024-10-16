from django.contrib.auth.models import User
from os import mkdir
from os.path import isfile, isdir
from shutil import copy
from sys import stdout

from .base_seeder import BaseSeeder
from food_delivery_app.settings import MEDIA_ROOT, BASE_DIR
from ....models import Profile, Address


class ProfileSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the profile data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting Profile instances")
        Profile.objects.all().delete()

    def create_records(self) -> None:
        print("Creating profile")

        data = [
            {"user": "alaya", "address": "Niš, Serbia", "image": "avatar1.jpg"},
            {
                "user": "kashton",
                "address": "Belgrade, Bulevar Zorana Djindjica 81, Serbia",
                "image": "avatar2.jpg",
            },
            {"user": "jamir", "address": "Belgrade, Aleksandra Fleminga 42, Serbia"},
            {"user": "mark", "address": "Moscow, Russia"},
        ]

        SOURCE_FOLDER_PATH = f"{BASE_DIR}/customer_part/static/customer_part/images/profile_images/"
        TARGET_FOLDER_PATH = f"{MEDIA_ROOT}profile_pictures/"

        if not isdir(TARGET_FOLDER_PATH):
            mkdir(TARGET_FOLDER_PATH)

        try:
            copy(src=f"{BASE_DIR}/customer_part/static/customer_part/images/avatar.png", dst=f"{TARGET_FOLDER_PATH}avatar.png")
            print("Copied the default avatar image")
        except PermissionError:
            print(
                f"You do not have the permissions to copy avatar.png"
            )
        except:
            print(f"There was while copying the avatar.png")

        for profile_data in data:
            user = User.objects.get(username=profile_data["user"])

            address = Address.objects.get(raw=profile_data["address"])
            profile = Profile(user=user, address=address)

            if profile_data.get("image"):
                if not isdir(TARGET_FOLDER_PATH):
                    mkdir(TARGET_FOLDER_PATH)

                SOURCE_FILE_PATH = f"{SOURCE_FOLDER_PATH}{profile_data['image']}"
                TARGET_FILE_PATH = f"{TARGET_FOLDER_PATH}{profile_data['image']}"

                if not isfile(TARGET_FILE_PATH):
                    try:
                        copy(src=SOURCE_FILE_PATH, dst=TARGET_FILE_PATH)
                    except PermissionError:
                        print(
                            f"You do not have the permissions to copy {profile_data['image']}"
                        )
                    except:
                        print(f"There was while copying the {profile_data['image']}")

                profile.image = profile_data["image"]

            profile.save()

            print(f"Profile for user {user} created.")
