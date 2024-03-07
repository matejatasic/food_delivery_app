from django.http import HttpRequest
from django.test import TestCase
from json import dumps
from unittest.mock import patch, Mock

from ..base import faker
from ...exceptions import (
    EmptyRequestBodyError,
    RestaurantDoesNotExist,
    RestaurantCategoryDoesNotExist,
)
from ..factories import RestaurantFactory, RestaurantLikeFactory, UserFactory
from ...models import Restaurant
from ...services.restaurant_service import RestaurantService, LIKED, UNLIKED


class RestaurantServiceTests(TestCase):
    restaurant_service = RestaurantService()

    @patch.object(RestaurantService, "get_restaurants_by_category_queryset")
    @patch.object(RestaurantService, "category_exists")
    def test_get_by_category_returns_results_when_category_exists_succesfully(
        self, category_exists_mock, get_restaurants_by_category_queryset_mock
    ):
        """Asserts that the method for getting the restaurants returns dictionaries if the category exists"""

        category_exists_mock.return_value = True
        number_of_restaurants = 3
        get_restaurants_by_category_queryset_mock.return_value = (
            RestaurantFactory.build_batch(number_of_restaurants)
        )

        result = self.restaurant_service.get_by_category(category_name=faker.pystr())

        self.assertEqual(len(result), number_of_restaurants)
        self.assertIsInstance(result[0], dict)

    @patch.object(RestaurantService, "category_exists")
    def test_get_by_category_raises_the_restaurant_category_does_not_exist_error(
        self, category_exists_mock
    ):
        """Asserts that the method for getting the restaurants raises the RestaurantCategoryDoesNotExist if the category does not exists"""

        category_exists_mock.side_effect = RestaurantCategoryDoesNotExist()

        self.assertRaises(
            RestaurantCategoryDoesNotExist,
            self.restaurant_service.get_by_category,
            category_name=faker.pystr(),
        )

    @patch.object(RestaurantService, "create_like")
    @patch.object(RestaurantService, "get_like")
    @patch.object(RestaurantService, "get_by_id_queryset")
    @patch.object(RestaurantService, "restaurant_exists")
    def test_like_liked_if_not_already_liked(
        self,
        restaurant_exists_mock,
        get_by_id_queryset_mock,
        get_like_mock,
        create_like_mock,
    ):
        """Assert that the like method likes the restaurant if it is not already liked by the user"""

        restaurant_exists_mock.return_value = True
        restaurant = RestaurantFactory()
        get_by_id_queryset_mock.return_value = restaurant
        get_like_mock.side_effect = Exception()
        create_like_mock.return_value = None
        self.__add_number_of_likes_to_restaurant(
            restaurant=restaurant, number_of_likes=1
        )
        request_mock = Mock(HttpRequest)
        request_mock.body = dumps({"restaurant_id": faker.random_digit()})
        request_mock.user = UserFactory()

        result = self.restaurant_service.like(request=request_mock)

        self.assertEqual(result[0], LIKED)

    @patch.object(RestaurantService, "get_like")
    @patch.object(RestaurantService, "get_by_id_queryset")
    @patch.object(RestaurantService, "restaurant_exists")
    def test_like_unliked_if_already_liked(
        self, restaurant_exists_mock, get_by_id_queryset_mock, get_like_mock
    ):
        """Assert that the like method unlikes the restaurant if it is already liked by the user"""

        restaurant_exists_mock.return_value = True
        restaurant = RestaurantFactory()
        get_by_id_queryset_mock.return_value = restaurant
        get_like_mock.return_value = Mock(RestaurantLikeFactory())
        self.__add_number_of_likes_to_restaurant(
            restaurant=restaurant, number_of_likes=1
        )
        request_mock = Mock(HttpRequest)
        request_mock.body = dumps({"restaurant_id": faker.random_digit()})
        request_mock.user = UserFactory()

        result = self.restaurant_service.like(request=request_mock)

        self.assertEqual(result[0], UNLIKED)

    def __add_number_of_likes_to_restaurant(
        self, restaurant: Restaurant, number_of_likes: int
    ):
        restaurant.number_of_likes = number_of_likes

    def test_like_raises_error_when_request_body_empty(self):
        """Asserts that the like method raises the EmptyRequestBodyError when request body is empty"""

        request_mock = Mock(HttpRequest)

        request_mock.body = None

        self.assertRaises(
            EmptyRequestBodyError, self.restaurant_service.like, request_mock
        )

    @patch.object(RestaurantService, "restaurant_exists")
    def test_like_raises_the_restaurant_does_not_exist_error(
        self, restaurant_exists_mock
    ):
        """Asserts that the method for getting the restaurants raises the RestaurantDoesNotExist if the restaurant does not exists"""

        restaurant_exists_mock.side_effect = RestaurantDoesNotExist()
        request_mock = Mock(HttpRequest)
        request_mock.body = dumps({"restaurant_id": faker.random_digit()})
        request_mock.user = UserFactory()

        self.assertRaises(
            RestaurantDoesNotExist, self.restaurant_service.like, request_mock
        )
