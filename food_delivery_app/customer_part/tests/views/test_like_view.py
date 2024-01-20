from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from json import dumps, loads

from ..factories import UserFactory, RestaurantFactory
from ...services.restaurant_service import LIKED


class LikeViewTest(TestCase):
    like_url: str = reverse("like")
    login_url: str = reverse("login")

    def test_like_successfully_likes_a_restaurant(self):
        """Asserts that the like view successfully likes the restaurant and returns the appropriate aciton"""

        user = UserFactory()
        restaurant = RestaurantFactory.create()

        self.client.force_login(user)

        response = self.client.post(
            self.like_url,
            dumps({"restaurant_id": restaurant.id}),
            content_type="application/json",
        )
        content = loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(content["action"], LIKED)
        self.assertEqual(content["current_number_of_likes"], 1)

    def test_like_returns_unauthorized_status_code_when_user_not_authenticated(self):
        """Asserts that the response has the Unauthorized status when user is not authenticated"""

        response = self.client.post(self.like_url, "", content_type="application/json")

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_like_returns_bad_request_status_code_when_get_request_sent(self):
        """Asserts that the response has the BadRequest status code when the GET request is sent"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(self.like_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_like_returns_bad_request_when_request_body_empty(self):
        """Asserts that the response contains the Bad request status code when the request body is empty"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(self.like_url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_like_returns_not_found_status_code_when_restaurant_does_not_exist(self):
        """Asserts that the response has the NotFound status code when the restaurant does not exist"""

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(
            self.like_url,
            dumps({"restaurant_id": 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
