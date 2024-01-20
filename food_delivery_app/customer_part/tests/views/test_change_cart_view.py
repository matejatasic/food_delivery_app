from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from json import dumps

from ..factories import UserFactory, RestaurantItemFactory
from ...services.cart_service import INCREMENT, DECREMENT


class ChangeCartViewTest(TestCase):
    change_cart_url = reverse("change_cart")

    def test_change_cart_increments_the_item_successfully(self):
        """Asserts that the change cart increments the item quantity in cart by 1"""

        user = UserFactory()
        item = RestaurantItemFactory.create()
        self.client.force_login(user)

        response = self.client.post(
            self.change_cart_url,
            dumps({"item_id": item.id, "action": INCREMENT}),
            content_type="application/json",
        )

        cart = self.client.session.get("cart")
        item_id = str(item.id)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(item_id, cart["items"])
        self.assertEqual(cart["total_number_of_items"], 1)
        self.assertEqual(cart["items"][item_id]["product"], item.name)
        self.assertEqual(cart["items"][item_id]["quantity"], 1)

    def test_change_cart_decrements_the_item_successfully(self):
        """Asserts that the change cart decrements the item quantity in cart by 1"""

        user = UserFactory()
        item = RestaurantItemFactory.create()
        self.client.force_login(user)

        self.client.post(
            self.change_cart_url,
            dumps({"item_id": item.id, "action": INCREMENT}),
            content_type="application/json",
        )
        response = self.client.post(
            self.change_cart_url,
            dumps({"item_id": item.id, "action": DECREMENT}),
            content_type="application/json",
        )

        cart = self.client.session.get("cart")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(cart["total_number_of_items"], 0)
        self.assertEqual(len(cart["items"].keys()), 0)

    def test_change_cart_returns_unauthorized_when_user_not_authenticated(self):
        """Asserts that the response contains the Unauthorized status code when user not authenticated"""

        response = self.client.post(self.change_cart_url)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_change_cart_returns_bad_code_when_get_request(self):
        """Asserts that the response contains the Bad request status code when the request method is GET"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(self.change_cart_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_cart_returns_bad_request_when_request_body_empty(self):
        """Asserts that the response contains the Bad request status code when the request body is empty"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(self.change_cart_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_cart_returns_bad_request_when_request_body_data_invalid(self):
        """Asserts that the response contains the Bad request status code when the request body is missing the needed fields"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(
            self.change_cart_url,
            "{}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_cart_returns_bad_request_when_action_invalid(self):
        """Asserts that the response contains the Bad request status code when the action is invalid"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(
            self.change_cart_url,
            '{"item_id": 1, "action": "invalid"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_cart_returns_bad_request_when_item_not_exists(self):
        """Asserts that the response contains the Bad request status code when the restaurant item does not exist"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(
            self.change_cart_url,
            dumps({"item_id": 1, "action": INCREMENT}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_cart_returns_bad_request_when_decrement_and_item_not_in_cart(self):
        """Asserts that the response contains the Bad request status code when the action is decrement and restaurant item is not in the cart"""

        user = UserFactory()
        item = RestaurantItemFactory.create()
        self.client.force_login(user)

        response = self.client.post(
            self.change_cart_url,
            dumps({"item_id": item.id, "action": DECREMENT}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
