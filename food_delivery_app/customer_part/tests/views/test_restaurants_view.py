from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from ..factories import RestaurantFactory


class RestaurantsViewTest(TestCase):
    restaurants_url: str = reverse("restaurants")

    def test_restaurants_view_returns_appropriate_view_data(self):
        number_of_items = 2

        RestaurantFactory.create_batch(2)
        response = self.client.get(self.restaurants_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["restaurants"]), number_of_items)
        self.assertEqual(len(response.context["categories"]), number_of_items)
