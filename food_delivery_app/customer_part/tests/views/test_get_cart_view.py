from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from json import dumps, loads

from ..factories import UserFactory, RestaurantItemFactory
from ...services.cart_service import INCREMENT

class GetCartViewTest(TestCase):
    get_cart_url = reverse("get_cart")
    change_cart_url = reverse("change_cart")

    def test_get_cart_successfully_returns_cart(self):
        """Asserts that the get cart view returns appropriate data"""

        number_of_items = 2

        user = UserFactory.create()
        items = RestaurantItemFactory.create_batch(number_of_items)

        self.client.force_login(user)

        self.client.post(
            self.change_cart_url,
            dumps({"item_id": items[0].id, "action": INCREMENT}),
            content_type="application/json",
        )
        self.client.post(
            self.change_cart_url,
            dumps({"item_id": items[1].id, "action": INCREMENT}),
            content_type="application/json",
        )

        response = self.client.get(self.get_cart_url)
        data = loads(response.content)["data"]

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertIn("cart", data)
        self.assertIn("price_for_all_items", data)
        self.assertIn("delivery", data)
        self.assertIn("tax", data)
        self.assertIn("total", data)

    def test_get_cart_returns_unauthorized_status_code_when_user_not_authenticated(self):
        """Asserts that the response has the Unauthorized status when user is not authenticated"""

        response = self.client.get(self.get_cart_url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)