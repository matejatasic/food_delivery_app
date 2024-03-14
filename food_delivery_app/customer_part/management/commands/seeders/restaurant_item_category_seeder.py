from sys import stdout

from .base_seeder import BaseSeeder
from ....models import Restaurant, RestaurantItemCategory


class RestaurantItemCategorySeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the restaurant item category data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting RestaurantItemCategory instances")
        RestaurantItemCategory.objects.all().delete()

    def create_records(self) -> None:
        print("Creating restaurant item category")

        data = [
            {"name": "Pizza 45cm", "restaurant": "La Strega"},
            {"name": "Pizza 22cm", "restaurant": "La Strega"},
            {"name": "Chicken Wings - 9 pieces", "restaurant": "Screaming Chicken"},
        ]

        for category_data in data:
            restaurant = Restaurant.objects.get(name=category_data["restaurant"])
            category = RestaurantItemCategory(
                name=category_data["name"], restaurant=restaurant
            )
            category.save()

            print(f"Restaurant item category {category} created.")
