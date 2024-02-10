from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from json import dumps

from ..factories import UserFactory, RestaurantItemFactory
from ...services.cart_service import INCREMENT


class CartViewTest(TestCase):
    cart_url = reverse("cart")
    change_cart_url = reverse("change_cart")

    def test_cart_returns_template_with_appropriate_context_data(self):
        """Asserts that the cart view returns appropriate data"""

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

        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("cart", response.context)
        self.assertIn("price_for_all_items", response.context)
        self.assertIn("delivery", response.context)
        self.assertIn("tax", response.context)
        self.assertIn("total", response.context)

    def test_cart_redirects_if_user_not_logged_in(self):
        """Asserts that the user is redirected if not logged in when sending to cart route"""

        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("login", response["location"])
