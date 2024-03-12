from django.contrib.auth.models import User
from sys import stdout

from .base_seeder import BaseSeeder
from ....models import Address


class AddressSeeder(BaseSeeder):
    help = "Seeds the database for easier development and testing"

    def handle(self, mode: str):
        stdout.write("\nStarted seeding the address data...")
        self.run_seed(mode)
        stdout.write("Finished seeding.\n")

    def run_seed(self, mode: str) -> None:
        self.clear_data()

        if mode == self.MODE_CLEAR:
            return

        self.create_records()

    def clear_data(self) -> None:
        print("\nDeleting Address instances")
        Address.objects.all().delete()

    def create_records(self) -> None:
        print("Creating address")

        data = [
            {
                "latitude": 44.7589,
                "longitude": 20.4167,
                "raw": "Belgrade, Spasovdanska 15, Serbia",
                "address_line": "Spasovdanska 15",
                "district_1": "Belgrade City",
                "district_2": "Belgrade",
                "country": "Serbia",
                "locality": "Belgrade",
            },
            {
                "latitude": 44.8125,
                "longitude": 20.4612,
                "raw": "Belgrade, Pajsijeva 15, Serbia",
                "address_line": "Pajsijeva 15",
                "district_1": "Belgrade City",
                "district_2": "Belgrade",
                "country": "Serbia",
                "locality": "Belgrade",
            },
            {
                "latitude": 44.8164,
                "longitude": 20.4185,
                "raw": "Belgrade, Bulevar Zorana Djindjica 81, Serbia",
                "address_line": "Bulevar Zorana Djindjica 81",
                "district_1": "Belgrade City",
                "district_2": "Belgrade",
                "country": "Serbia",
                "locality": "Belgrade",
            },
            {
                "latitude": 44.8072,
                "longitude": 20.5159,
                "raw": "Belgrade, Aleksandra Fleminga 42, Serbia",
                "address_line": "Aleksandra Fleminga 42",
                "district_1": "Belgrade City",
                "district_2": "Belgrade",
                "country": "Serbia",
                "locality": "Belgrade",
            },
            {
                "latitude": 55.75654221,
                "longitude": 37.61492157,
                "raw": "Moscow, Russia",
                "address_line": "",
                "district_1": "Moscow City",
                "district_2": "Moscow",
                "country": "Russia",
                "locality": "Moscow",
            },
            {
                "latitude": 43.2089,
                "longitude": 21.8954,
                "raw": "Niš, Serbia",
                "address_line": "",
                "district_1": "SER",
                "district_2": "Nišava District",
                "country": "Serbia",
                "locality": "Niš",
            },
            {
                "latitude": 47.4929,
                "longitude": 19.0528,
                "raw": "Budapest, Vaci utca 27, Hungary",
                "address_line": "Vaci utca 27",
                "district_1": "Budapest City",
                "district_2": "Budapest",
                "country": "Hungary",
                "locality": "Budapest",
            },
            {
                "latitude": 44.8122,
                "longitude": 20.4663,
                "raw": "Belgrade, Makedonska 28, Serbia",
                "address_line": "Makedonska 28",
                "district_1": "Belgrade City",
                "district_2": "Belgrade",
                "country": "Serbia",
                "locality": "Belgrade",
            },
            {
                "latitude": 32.0901,
                "longitude": 34.7334,
                "raw": "Tel Aviv, Ben Yehuda St 177, Israel",
                "address_line": "Ben Yehuda St 177",
                "district_1": "Tel Aviv City",
                "district_2": "Tel Aviv",
                "country": "Israel",
                "locality": "Tel Aviv",
            },
        ]

        for address_data in data:
            address = Address(**address_data)
            address.save()

            print(f"Address {address} created.")
