from django.core.management.base import BaseCommand

from .seeders.address_seeder import AddressSeeder
from .seeders.base_seeder import BaseSeeder
from .seeders.group_seeder import GroupSeeder
from .seeders.order_seeder import OrderSeeder
from .seeders.order_item_seeder import OrderItemSeeder
from .seeders.profile_seeder import ProfileSeeder
from .seeders.restaurant_seeder import RestaurantSeeder
from .seeders.restaurant_category_seeder import RestaurantCategorySeeder
from .seeders.restaurant_item_seeder import RestaurantItemSeeder
from .seeders.restaurant_item_category_seeder import RestaurantItemCategorySeeder
from .seeders.user_seeder import UserSeeder

""" Clear all data and creates addresses """
MODE_REFRESH = "refresh"

""" Clear all data and do not create any object """
MODE_CLEAR = "clear"


class Command(BaseCommand):
    help = "seed database for testing and development."
    seeders: list[BaseSeeder] = [
        GroupSeeder(),
        UserSeeder(),
        AddressSeeder(),
        ProfileSeeder(),
        RestaurantCategorySeeder(),
        RestaurantSeeder(),
        RestaurantItemCategorySeeder(),
        RestaurantItemSeeder(),
        OrderSeeder(),
        OrderItemSeeder(),
    ]

    def add_arguments(self, parser) -> None:
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options) -> None:
        self.stdout.write("Started seeding the data...")
        self.run_seed(options["mode"])
        self.stdout.write("\nFinished seeding.\n")

    def run_seed(self, mode) -> None:
        for seeder in self.seeders:
            seeder.handle(mode=mode)
