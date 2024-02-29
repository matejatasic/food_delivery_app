from dataclasses import dataclass, field
from datetime import datetime
from functools import reduce
from django.core.serializers import serialize
from django.db.models.query import QuerySet

from .models import Address, RestaurantItem, RestaurantItemCategory, OrderItem
from .types import OrderItemDto


class AddressOptionDto:
    def __init__(self, address: Address) -> None:
        self.__address_model = address
        self.__address = address.raw

    def get_dict(self):
        return {"id": serialize("json", [self.__address_model]), "text": self.__address}

    @property
    def pk(self):
        return self.__address_model

    @property
    def address(self):
        return self.__address

    def __str__(self) -> str:
        return self.__address


class MapsResponseResourcesDto:
    __bbox: list[int]
    __address: "MapsResponseAddressDto"

    def __init__(self, bbox: list[int], address_information: dict) -> None:
        self.__bbox = bbox
        self.__address = MapsResponseAddressDto(
            formatted_address=address_information["formattedAddress"],
            address_line=address_information.get("addressLine", None),
            district_1=address_information.get("adminDistrict", ""),
            district_2=address_information.get("adminDistrict2", ""),
            country_region=address_information["countryRegion"],
            locality=address_information.get("locality", ""),
            postal_code=address_information.get("postalCode", None),
        )

    @property
    def latitude(self):
        return self.__bbox[0]

    @property
    def longitude(self):
        return self.__bbox[1]

    @property
    def formatted_address(self):
        return self.__address.formatted_address

    @property
    def address_line(self) -> str | None:
        return self.__address.address_line

    @property
    def district_1(self) -> str:
        return self.__address.district_1

    @property
    def district_2(self) -> str:
        return self.__address.district_2

    @property
    def country_region(self) -> str:
        return self.__address.country_region

    @property
    def locality(self) -> str:
        return self.__address.locality

    @property
    def postal_code(self) -> str | None:
        return self.__address.postal_code


class MapsResponseAddressDto:
    __formatted_address: str
    __address_line: str | None
    __district_1: str
    __district_2: str
    __country_region: str
    __locality: str
    __postal_code: str | None

    def __init__(
        self,
        formatted_address: str,
        address_line: str | None,
        district_1: str,
        district_2: str,
        country_region: str,
        locality: str,
        postal_code: str | None,
    ) -> None:
        self.__formatted_address = formatted_address
        self.__address_line = address_line
        self.__district_1 = district_1
        self.__district_2 = district_2
        self.__country_region = country_region
        self.__locality = locality
        self.__postal_code = postal_code

    @property
    def formatted_address(self) -> str:
        return self.__formatted_address

    @property
    def address_line(self) -> str | None:
        return self.__address_line

    @property
    def district_1(self) -> str:
        return self.__district_1

    @property
    def district_2(self) -> str:
        return self.__district_2

    @property
    def country_region(self) -> str:
        return self.__country_region

    @property
    def locality(self) -> str:
        return self.__locality

    @property
    def postal_code(self) -> str | None:
        return self.__postal_code


@dataclass
class RestaurantDto:
    id: int
    name: str
    description: str
    image: str
    number_of_likes: int
    food_items: list[RestaurantItem] | None = None
    food_item_categories: list[RestaurantItemCategory] | None = None

    def get_dict(self) -> dict[str, str | int | object]:
        dictionary = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "number_of_likes": self.number_of_likes,
        }

        if not self.food_items is None:
            dictionary["food_items"] = self.food_items

        if not self.food_item_categories is None:
            dictionary["food_item_categories"] = self.food_item_categories

        return dictionary


class OrderShowDto:
    status: str
    _date_ordered: str = field(init=False, repr=False)
    _order_items: list[OrderItemDto] = field(init=False, repr=False)
    _price: float = field(init=False, repr=False)

    def __init__(
        self, date_ordered: datetime, order_items: QuerySet[OrderItem], status: str
    ) -> None:
        self.date_ordered = date_ordered
        self.order_items = order_items
        self.price = order_items
        self.status = status

    @property
    def date_ordered(self):
        return self._date_ordered

    @date_ordered.setter
    def date_ordered(self, created_at: datetime):
        self._date_ordered = f"{created_at.year}-{created_at.month}-{created_at.day}"

    @property
    def order_items(self):
        return self._order_items

    @order_items.setter
    def order_items(self, order_items: QuerySet[OrderItem]):
        self._order_items = [
            {"name": order_item.item.name, "quantity": order_item.quantity}
            for order_item in order_items
        ]

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, order_items: QuerySet[OrderItem]):
        self._price = reduce(
            lambda accumulator, order_item: accumulator + float(order_item.item.price),
            order_items,
            0.0,
        )


class PendingOrderShowDto(OrderShowDto):
    id: int
    user: str
    restaurant: str
    address: str

    def __init__(
        self,
        id: int,
        user: str,
        restaurant: str,
        address: str,
        date_ordered: datetime,
        order_items: QuerySet[OrderItem],
        status: str,
    ) -> None:
        self.id = id
        self.user = user
        self.restaurant = restaurant
        self.address = address
        super().__init__(date_ordered, order_items, status)


class DriverOrderShowDto(OrderShowDto):
    id: int
    user: str
    restaurant_names: list[str]
    restaurant_addresses: list[str]
    restaurant_coordinates: list[tuple[float, float]]
    customer_coordinates: tuple[float, float]
    address: str
    latitude: float
    longitude: float

    def __init__(
        self,
        id: int,
        user: str,
        restaurant_names: list[str],
        restaurant_addresses: list[str],
        restaurant_coordinates: list[tuple[float, float]],
        customer_coordinates: tuple[float, float],
        address: str,
        date_ordered: datetime,
        order_items: QuerySet[OrderItem],
        status: str,
        latitude: float,
        longitude: float,
    ) -> None:
        self.id = id
        self.user = user
        self.restaurant_names = restaurant_names
        self.restaurant_addresses = restaurant_addresses
        self.restaurant_coordinates = restaurant_coordinates
        self.customer_coordinates = customer_coordinates
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

        super().__init__(date_ordered, order_items, status)
