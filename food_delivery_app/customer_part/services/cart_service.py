from django.core.exceptions import FieldDoesNotExist, FieldError
from django.http import HttpRequest
from json import loads

from ..exceptions import RestaurantItemDoesNotExist, RestaurantItemNotInCart
from .restaurant_service import RestaurantService


INCREMENT = "increment"
DECREMENT = "decrement"

class CartService:
    def add_item(self, request: HttpRequest):
        data = loads(request.body)
        item_id = data.get("item_id")
        action = data.get("action")

        if not item_id or not action:
            raise FieldDoesNotExist("The request body needs to contain the \"item_id\" and \"action\" fields")

        if not action in (INCREMENT, DECREMENT):
            raise FieldError(f"The action can either be {INCREMENT} or {DECREMENT}")

        restaurant_service = RestaurantService()

        if not restaurant_service.item_exists(id=item_id):
            raise RestaurantItemDoesNotExist(f"The item with the id {item_id} does not exist")

        cart = request.session.get("cart", {"items": {}, "total_number_of_items": 0})
        items = cart["items"]
        cart_item = items.get(item_id)
        item = restaurant_service.get_item(id=item_id)

        if action == INCREMENT:
            if not cart_item:
                items[item_id] = {"product": item.name, "quantity": 0}

            items[item_id]["quantity"] += 1
            cart["total_number_of_items"] += 1

        if action == DECREMENT:
            if not cart_item:
                raise RestaurantItemNotInCart("The restaurant item is not present in the cart")

            items[item_id]["quantity"] -= 1
            cart["total_number_of_items"] -= 1

            if items[item_id]["quantity"] == 0:
                del items[item_id]

        request.session["cart"] = cart

        return (item.name, cart["total_number_of_items"])





