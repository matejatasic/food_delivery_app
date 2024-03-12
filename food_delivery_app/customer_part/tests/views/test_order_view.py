from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from random import randrange

from ..factories import UserFactory, RestaurantItemFactory
from ...models import Order


class OrderViewTest(TestCase):
    create_order_url: str = reverse("create_order")

    def test_create_creating_order_successfully(self):
        """Asserts that the create order view successfully creates the order"""

        restaurant_items = RestaurantItemFactory.create_batch(2)
        user = UserFactory()

        self.client.force_login(user)
        cart = {"items": {}, "total_number_of_items": 0}

        for item in restaurant_items:
            quantity = randrange(1, 10)

            cart["items"][item.id] = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": float(item.price),
                "image": item.image.name,
                "quantity": quantity,
            }
            cart["total_number_of_items"] += quantity

        self.client.session["cart"] = cart

        response = self.client.post(self.create_order_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_returns_unauthorized_status_code_when_user_not_authenticated(
        self,
    ):
        """Asserts that the response has the Unauthorized status when user is not authenticated"""

        response = self.client.post(self.create_order_url)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_create_order_returns_bad_request_status_code_when_get_request_sent(self):
        """Asserts that the response has the BadRequest status code when the GET request is sent"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(self.create_order_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
