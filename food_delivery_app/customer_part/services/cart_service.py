from django.core.exceptions import FieldDoesNotExist, FieldError
from django.http import HttpRequest
from json import JSONDecodeError, loads
from typing import cast

from ..exceptions import (
    RestaurantItemDoesNotExist,
    RestaurantItemNotInCart,
    EmptyRequestBodyError,
)
from ..models import RestaurantItem
from .restaurant_service import RestaurantService


INCREMENT = "increment"
DECREMENT = "decrement"


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
        items = cast(dict[str, dict[str, str | int]], cart["items"])
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

    def get_cart(
        self, request: HttpRequest
    ) -> dict[str, dict[str, dict[str, str | int]] | int]:
        return request.session.get("cart", {"items": {}, "total_number_of_items": 0})

    def set_cart(
        self,
        request: HttpRequest,
        cart: dict[str, dict[str, dict[str, str | int]] | int],
    ) -> None:
        request.session["cart"] = cart

    def get_item(self, id: str) -> RestaurantItem:
        restaurant_service = RestaurantService()

        return restaurant_service.get_item(id=id)

    def increment_item(
        self,
        cart_item: dict[str, str | int] | None,
        items: dict[str, dict[str, str | int]],
        item_id: str,
        item: RestaurantItem,
        cart: dict[str, dict | int],
    ) -> None:
        if not cart_item:
            items[item_id] = {"product": item.name, "quantity": 0}

        quantity: int = cast(int, items[item_id]["quantity"])
        total_number_of_items: int = cast(int, cart["total_number_of_items"])

        quantity += 1
        total_number_of_items += 1
        cart["total_number_of_items"] = total_number_of_items
        items[item_id]["quantity"] = quantity

    def decrement_item(
        self,
        cart_item: dict[str, str | int] | None,
        items: dict[str, dict[str, str | int]],
        item_id: str,
        cart: dict[str, dict | int],
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
