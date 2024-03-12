from django.contrib.auth.models import User
from sys import stdout

from .base_seeder import BaseSeeder
from ....models import Order, OrderStatus


class OrderSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the order data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting Order instances")
        Order.objects.all().delete()

    def create_records(self) -> None:
        print("Creating order")

        data = [
            {"user": "kashton", "status": OrderStatus.ORDERED},
            {"user": "jamir", "status": OrderStatus.ORDERED},
        ]

        for order_data in data:
            user = User.objects.get(
                username=order_data["user"],
            )
            order = Order(buyer=user, status=order_data["status"])
            order.save()

            print(f"Order {order} created.")
