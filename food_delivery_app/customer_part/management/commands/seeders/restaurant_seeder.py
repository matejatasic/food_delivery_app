from os import mkdir
from os.path import isfile, isdir
from shutil import copy
from sys import stdout

from .base_seeder import BaseSeeder
from food_delivery_app.settings import MEDIA_ROOT, BASE_DIR
from ....models import Restaurant, RestaurantCategory, Address


class RestaurantSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the restaurant data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting Restaurant instances")
        Restaurant.objects.all().delete()

    def create_records(self) -> None:
        print("Creating restaurant")

        data = [
            {
                "name": "Bash Smash Burgers",
                "description": "Bash Smash Burgers & Chicken - the place of delicious burgers",
                "image": "burger.jpg",
                "category": "Fast Food",
                "address": "Belgrade, Spasovdanska 15, Serbia",
            },
            {
                "name": "La Strega",
                "description": "The kingdom of pizza!",
                "image": "pizza.jpeg",
                "category": "Pizzerias",
                "address": "Belgrade, Pajsijeva 15, Serbia",
            },
            {
                "name": "Screaming Chicken",
                "description": "The best chicken wings in town!",
                "image": "screaming_chicken.jpeg",
                "category": "Fast Food",
                "address": "Belgrade, Makedonska 28, Serbia",
            },
            {
                "name": "KFC",
                "description": "So good that it looks to good to be true!",
                "image": "kfc.jpeg",
                "category": "Fast Food",
                "address": "Budapest, Vaci utca 27, Hungary",
            },
            {
                "name": "Wok Republic",
                "description": "Asian fast food",
                "image": "wok-republic.jpeg",
                "category": "Fast casual",
                "address": "Tel Aviv, Ben Yehuda St 177, Israel",
            },
        ]

        for restaurant_data in data:
            SOURCE_FOLDER_PATH = f"{BASE_DIR}/customer_part/static/customer_part/images/restaurant_images/"
            TARGET_FOLDER_PATH = f"{MEDIA_ROOT}restaurant_pictures/"

            SOURCE_FILE_PATH = f"{SOURCE_FOLDER_PATH}{restaurant_data['image']}"
            TARGET_FILE_PATH = f"{TARGET_FOLDER_PATH}{restaurant_data['image']}"

            if not isdir(TARGET_FOLDER_PATH):
                mkdir(TARGET_FOLDER_PATH)

            if not isfile(TARGET_FILE_PATH):
                try:
                    copy(src=SOURCE_FILE_PATH, dst=TARGET_FILE_PATH)
                except PermissionError:
                    print(
                        f"You do not have the permissions to copy {restaurant_data['image']}"
                    )
                except:
                    print(f"There was while copying the {restaurant_data['image']}")

            category = RestaurantCategory.objects.get(name=restaurant_data["category"])
            address = Address.objects.get(raw=restaurant_data["address"])
            restaurant = Restaurant(
                name=restaurant_data["name"],
                description=restaurant_data["description"],
                image=restaurant_data["image"],
                category=category,
                address=address,
            )
            restaurant.save()

            print(f"Restaurant {restaurant} created.")
