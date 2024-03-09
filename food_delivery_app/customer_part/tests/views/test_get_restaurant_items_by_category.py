from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from json import loads

from ..factories import UserFactory, RestaurantItemFactory


class GetRestaurantItemsByCategoryViewTest(TestCase):
    get_restaurant_items_by_category_url = reverse("get_restaurant_items_by_category")

    def test_get_restaurant_items_by_category_returns_items_successfully(self):
        """Asserts that the response contains at least one item"""

        user = UserFactory()
        items = RestaurantItemFactory.create_batch(3)

        self.client.force_login(user)

        response = self.client.get(
            f"{self.get_restaurant_items_by_category_url}?category_name={items[0].category.name}"
        )
        content = loads(response.content)

        data = loads(content["data"])

        self.assertGreaterEqual(1, len(data))

    def test_get_restaurant_items_by_category_returns_bad_request_status_code_when_post_request_sent(
        self,
    ):
        """Asserts that the response has the BadRequest status code when the POST request is sent"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(self.get_restaurant_items_by_category_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_restaurant_items_by_category_returns_not_found_status_code_when_restaurant_item_category_does_not_exist(
        self,
    ):
        """Asserts that the response has the NotFound status code when the restaurant item category does not exist"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(
            f"{self.get_restaurant_items_by_category_url}?category_name=1"
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
