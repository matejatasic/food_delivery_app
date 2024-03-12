from os import mkdir
from os.path import isfile, isdir
from shutil import copy
from sys import stdout
from typing import cast

from .base_seeder import BaseSeeder
from food_delivery_app.settings import MEDIA_ROOT, BASE_DIR
from ....models import Restaurant, RestaurantItemCategory, RestaurantItem


class RestaurantItemSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the restaurant item data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting RestaurantItem instances")
        RestaurantItem.objects.all().delete()

    def create_records(self) -> None:
        print("Creating restaurant item")

        data = [
            {
                "name": "Frutti di mare pizza",
                "category": "Pizza 22cm",
                "restaurant": "La Strega",
                "description": "Fresh seafood meets pizza. Transport yourself to the coast, with this Frutti De Mare Pizza",
                "price": 12.00,
                "image": "frutti_di_mare_pizza.jpeg",
            },
            {
                "name": "Quattro Garni pizza",
                "category": "Pizza 22cm",
                "restaurant": "La Strega",
                "description": "If you're looking for an ultra cheesy pizza then look no further than this classic!",
                "price": 10.00,
                "image": "quattro_garni_pizza.jpeg",
            },
            {
                "name": "Amos pizza",
                "category": "Pizza 45cm",
                "restaurant": "La Strega",
                "description": "A very good pizza.",
                "price": 18.00,
                "image": "amos_pizza.jpeg",
            },
            {
                "name": "Chicken Wings",
                "category": "Chicken Wings - 9 pieces",
                "restaurant": "Screaming Chicken",
                "description": "Chicken wings cooked with hot air without oil.",
                "price": 10.00,
                "image": "chicken-wings.jpg",
            },
        ]

        for item_data in data:
            restaurant = Restaurant.objects.get(name=item_data["restaurant"])
            category = RestaurantItemCategory.objects.get(name=item_data["category"])

            SOURCE_FOLDER_PATH = (
                f"{BASE_DIR}/customer_part/static/customer_part/images/item_images/"
            )
            TARGET_FOLDER_PATH = f"{MEDIA_ROOT}restaurant_items/"

            if not isdir(TARGET_FOLDER_PATH):
                mkdir(TARGET_FOLDER_PATH)

            SOURCE_FILE_PATH = f"{SOURCE_FOLDER_PATH}{item_data['image']}"
            TARGET_FILE_PATH = f"{TARGET_FOLDER_PATH}{item_data['image']}"

            if not isfile(TARGET_FILE_PATH):
                try:
                    copy(src=SOURCE_FILE_PATH, dst=TARGET_FILE_PATH)
                except PermissionError:
                    print(
                        f"You do not have the permissions to copy {item_data['image']}"
                    )
                except:
                    print(f"There was while copying the {item_data['image']}")

            item = RestaurantItem(
                name=cast(str, item_data["name"]),
                description=cast(str, item_data["description"]),
                category=category,
                restaurant=restaurant,
                price=cast(str, item_data["price"]),
                image=item_data["image"],
            )
            item.save()

            print(f"Restaurant item {item} created.")
