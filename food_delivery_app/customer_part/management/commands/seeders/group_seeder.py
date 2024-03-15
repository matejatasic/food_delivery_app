from django.contrib.auth.models import Group
from sys import stdout

from .base_seeder import BaseSeeder


class GroupSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the group data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting Group instances")
        Group.objects.all().delete()

    def create_records(self) -> None:
        print("Creating group")

        data = ["Admin", "Customer", "Driver"]

        for group_name in data:
            group = Group(name=group_name)
            group.save()

            print(f"Group {group} created.")
