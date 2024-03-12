from django.contrib.auth.models import User
from sys import stdout

from .base_seeder import BaseSeeder
from ....models import RestaurantCategory


class RestaurantCategorySeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the restaurant category data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting RestaurantCategory instances")
        RestaurantCategory.objects.all().delete()

    def create_records(self) -> None:
        print("Creating restaurant category")

        data = [{"name": "Pizzerias"}, {"name": "Fast Food"}, {"name": "Fast casual"}]

        for category_data in data:
            category = RestaurantCategory(name=category_data["name"])
            category.save()

            print(f"Restaurant category {category} created.")
