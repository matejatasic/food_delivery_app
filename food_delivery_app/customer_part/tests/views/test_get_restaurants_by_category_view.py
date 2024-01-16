from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from json import loads

from ..factories import UserFactory, RestaurantFactory


class GetRestaurantsByCategoryViewTest(TestCase):
    get_restaurants_by_category_url: str = reverse("get_restaurants_by_category")

    def test_get_restaurants_by_category_returns_restaurants_successfully(self):
        """Asserts that the response contains at least one restaurant"""

        user = UserFactory()
        restaurants = RestaurantFactory.create_batch(3)

        self.client.force_login(user)

        response = self.client.get(
            f"{self.get_restaurants_by_category_url}?category_name={restaurants[0].category.name}"
        )
        content = loads(response.content)
        data = loads(content["data"])

        self.assertGreaterEqual(1, len(data))

    def test_get_restaurants_by_category_returns_unauthorized_status_code_when_user_not_authenticated(
        self,
    ):
        """Asserts that the response has the Unauthorized status when user is not authenticated"""

        response = self.client.get(self.get_restaurants_by_category_url)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_get_restaurants_by_category_returns_bad_request_status_code_when_post_request_sent(
        self,
    ):
        """Asserts that the response has the BadRequest status code when the POST request is sent"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(self.get_restaurants_by_category_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_restaurants_by_category_returns_not_found_status_code_when_restaurant_does_not_exist(
        self,
    ):
        """Asserts that the response has the NotFound status code when the restaurant category does not exist"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(
            f"{self.get_restaurants_by_category_url}?category_name=1"
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
