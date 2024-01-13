from django.core.exceptions import FieldDoesNotExist, FieldError
from django.http import HttpRequest
from django.test import TestCase
from json import dumps
from unittest.mock import Mock, patch

from ...exceptions import EmptyRequestBodyError, RestaurantItemDoesNotExist, RestaurantItemNotInCart
from ..factories import RestaurantItemFactory
from ...services.cart_service import CartService, INCREMENT, DECREMENT


class CartServiceTests(TestCase):
    cart_service = CartService()

    @patch.object(CartService, "get_item")
    @patch.object(CartService, "item_exists")
    def test_change_cart_increments_the_cart_successfully(
        self, item_exists_mock, get_item_mock
    ):
        """Asserts that the change cart method increments the item in the cart by one"""

        request_mock = Mock(HttpRequest)
        item = RestaurantItemFactory()

        request_mock.body = dumps({"item_id": item.id, "action": INCREMENT})
        request_mock.session = {}
        item_exists_mock.return_value = True
        get_item_mock.return_value = item

        self.cart_service.add_item(request_mock)

        cart = request_mock.session.get("cart")
        item_id: str = str(item.id)

        self.assertIn(item_id, cart["items"])
        self.assertEqual(cart["total_number_of_items"], 1)
        self.assertEqual(cart["items"][item_id]["product"], item.name)
        self.assertEqual(cart["items"][item_id]["quantity"], 1)

    @patch.object(CartService, "get_item")
    @patch.object(CartService, "item_exists")
    def test_change_cart_decrements_the_cart_successfully(
        self, item_exists_mock, get_item_mock
    ):
        """Asserts that the change cart method decrements the item in the cart by one"""

        request_mock = Mock(HttpRequest)
        item = RestaurantItemFactory()

        request_mock.body = dumps({"item_id": item.id, "action": DECREMENT})
        request_mock.session = {
            "cart": {
                "items": {f"{item.id}": {"product": item.name, "quantity": 1}},
                "total_number_of_items": 1,
            }
        }

        item_exists_mock.return_value = True
        get_item_mock.return_value = item

        self.cart_service.add_item(request_mock)

        cart = request_mock.session.get("cart")

        self.assertEqual(cart["total_number_of_items"], 0)
        self.assertEqual(len(cart["items"].keys()), 0)

    def test_change_cart_raises_error_when_request_body_empty(self):
        """Asserts that the change cart method raises the EmptyRequestBodyError when request body is empty"""

        request_mock = Mock(HttpRequest)

        request_mock.body = None

        self.assertRaises(EmptyRequestBodyError, self.cart_service.add_item, request_mock)

    def test_change_cart_raises_error_when_request_body_data_invalid(self):
        """Asserts that the change cart method raises the FieldDoesNotExist when request body data is invalid"""

        request_mock = Mock(HttpRequest)

        request_mock.body = "{}"

        self.assertRaises(FieldDoesNotExist, self.cart_service.add_item, request_mock)

    def test_change_cart_raises_error_when_action_invalid(self):
        """Asserts that the change cart method raises the FieldDoesNotExist when action is invalid"""

        request_mock = Mock(HttpRequest)

        request_mock.body = dumps({"item_id": 1, "action": "invalid"})

        self.assertRaises(FieldError, self.cart_service.add_item, request_mock)

    @patch.object(CartService, "item_exists")
    def test_change_cart_raises_error_when_item_not_exists(self, item_exists_mock):
        """Asserts that the change cart method raises the RestaurantItemDoesNotExist when restaurant item does not exist in the database"""

        request_mock = Mock(HttpRequest)

        request_mock.body = dumps({"item_id": 1, "action": INCREMENT})
        item_exists_mock.return_value = False

        self.assertRaises(RestaurantItemDoesNotExist, self.cart_service.add_item, request_mock)

    @patch.object(CartService, "get_item")
    @patch.object(CartService, "item_exists")
    def test_change_cart_raises_error_when_decrement_and_item_not_in_cart(
        self, item_exists_mock, get_item_mock
    ):
        """Asserts that the change cart method raises the RestaurantItemNotInCart when restaurant item is not in the cart"""

        request_mock = Mock(HttpRequest)
        item = RestaurantItemFactory()

        request_mock.body = dumps({"item_id": item.id, "action": DECREMENT})
        request_mock.session = {}
        item_exists_mock.return_value = True
        get_item_mock.return_value = item

        self.assertRaises(RestaurantItemNotInCart, self.cart_service.add_item, request_mock)