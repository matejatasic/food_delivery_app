from decimal import Decimal
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.forms import ImageField
from django.http import HttpRequest
from json import JSONDecodeError, loads
from typing import cast, NewType

from ..exceptions import (
    RestaurantItemDoesNotExist,
    RestaurantItemNotInCart,
    EmptyRequestBodyError,
)
from ..models import RestaurantItem
from .restaurant_service import RestaurantService


INCREMENT = "increment"
DECREMENT = "decrement"

ItemDictionary = NewType("ItemDictionary", dict[str, str | int | Decimal | ImageField])
ItemsDictionary = NewType("ItemsDictionary", dict[str, ItemDictionary])
Cart = NewType("Cart", dict[str, ItemsDictionary | int | float])


class CartService:
    def add_item(self, request: HttpRequest):
        try:
            data = loads(request.body)
        except JSONDecodeError:
            raise EmptyRequestBodyError("The request body cannot be empty")
        except TypeError:
            raise EmptyRequestBodyError("The request body cannot be empty")

        item_id: str = str(data.get("item_id"))
        action: str = data.get("action")

        if not item_id or not action:
            raise FieldDoesNotExist(
                'The request body needs to contain the "item_id" and "action" fields'
            )

        if not action in (INCREMENT, DECREMENT):
            raise FieldError(f"The action can either be {INCREMENT} or {DECREMENT}")

        if not self.item_exists(id=item_id):
            raise RestaurantItemDoesNotExist(
                f"The item with the id {item_id} does not exist"
            )

        cart = self.get_cart(request=request)
        items = cast(ItemsDictionary, cart["items"])
        cart_item = items.get(item_id)
        item = self.get_item(id=item_id)

        if action == INCREMENT:
            self.increment_item(
                cart_item=cart_item, items=items, item_id=item_id, item=item, cart=cart
            )

        if action == DECREMENT:
            self.decrement_item(
                cart_item=cart_item, items=items, item_id=item_id, cart=cart
            )

        self.set_cart(request=request, cart=cart)

        return (item.name, cart["total_number_of_items"])

    def item_exists(self, id: str) -> bool:
        restaurant_service = RestaurantService()

        return restaurant_service.item_exists(id=id)

    def get_cart(self, request: HttpRequest) -> Cart:
        return request.session.get(
            "cart", {"items": {}, "total_number_of_items": 0, "delivery": 15.0}
        )

    def set_cart(
        self,
        request: HttpRequest,
        cart: Cart,
    ) -> None:
        request.session["cart"] = cart

    def increment_item(
        self,
        cart_item: ItemDictionary | None,
        items: ItemsDictionary,
        item_id: str,
        item: RestaurantItem,
        cart: Cart,
    ) -> None:
        if not cart_item:
            items[item_id] = cast(
                ItemDictionary,
                {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "price": float(item.price),
                    "image": item.image.name,
                    "quantity": 0,
                },
            )

        quantity: int = cast(int, items[item_id]["quantity"])
        total_number_of_items: int = cast(int, cart["total_number_of_items"])

        quantity += 1
        total_number_of_items += 1
        cart["total_number_of_items"] = total_number_of_items
        items[item_id]["quantity"] = quantity

    def decrement_item(
        self,
        cart_item: ItemDictionary | None,
        items: ItemsDictionary,
        item_id: str,
        cart: Cart,
    ) -> None:
        if not cart_item:
            raise RestaurantItemNotInCart(
                "The restaurant item is not present in the cart"
            )

        quantity: int = cast(int, items[item_id]["quantity"])
        total_number_of_items: int = cast(int, cart["total_number_of_items"])

        quantity -= 1
        total_number_of_items -= 1
        cart["total_number_of_items"] = total_number_of_items
        items[item_id]["quantity"] = quantity

        if items[item_id]["quantity"] == 0:
            del items[item_id]

    def get_cart_expenses(self, request) -> tuple[float, float, float, float]:
        cart: Cart = self.get_cart(request=request)

        price_for_all_items = self.get_price_for_all_items(cart=cart)
        delivery = cast(float, cart["delivery"])
        tax_rate = 0.1
        tax = price_for_all_items * tax_rate
        tax = float(f"{tax:.2f}")
        total = price_for_all_items + delivery + tax

        return (price_for_all_items, delivery, tax, total)

    def get_price_for_all_items(self, cart: Cart) -> float:
        if not cart["total_number_of_items"]:
            return 0.0

        price = 0.0
        cart_items = cast(ItemsDictionary, cart["items"])
        for item in cart_items.values():
            item_price = cast(float, item["price"])
            item_quantity = cast(int, item["quantity"])

            price += item_price * item_quantity

        return price

    def get_item(self, id: str) -> RestaurantItem:
        restaurant_service = RestaurantService()

        return restaurant_service.get_item(id=id)
