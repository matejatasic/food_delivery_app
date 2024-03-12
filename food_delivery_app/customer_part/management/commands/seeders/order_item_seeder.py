from django.contrib.auth.models import User
from sys import stdout
from typing import cast

from .base_seeder import BaseSeeder
from ....models import OrderItem, Order, RestaurantItem


class OrderItemSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the order item data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting OrderItem instances")
        OrderItem.objects.all().delete()

    def create_records(self) -> None:
        print("Creating order item")

        data = [
            {"user": "kashton", "item": "Amos pizza", "quantity": 1},
            {"user": "kashton", "item": "Quattro Garni pizza", "quantity": 1},
            {"user": "jamir", "item": "Frutti di mare pizza", "quantity": 2},
            {"user": "jamir", "item": "Chicken Wings", "quantity": 1},
        ]

        for item_data in data:
            order = Order.objects.get(buyer__username=item_data["user"])
            restaurant_item = RestaurantItem.objects.get(name=item_data["item"])
            item = OrderItem(
                order=order,
                item=restaurant_item,
                quantity=cast(int, item_data["quantity"]),
            )
            item.save()

            print(f"Order item {item} created.")
