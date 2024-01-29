from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from json import JSONDecodeError, loads
from typing import cast

from ..dtos import RestaurantDto
from ..exceptions import (
    EmptyRequestBodyError,
    RestaurantDoesNotExist,
    RestaurantCategoryDoesNotExist,
    RestaurantItemCategoryDoesNotExist,
)
from ..models import (
    Restaurant,
    RestaurantCategory,
    RestaurantLike,
    RestaurantItem,
    RestaurantItemCategory,
)


LIKED = "liked"
UNLIKED = "unliked"


class RestaurantService:
    def get_all(self) -> list[dict[str, str | int | object]]:
        return [
            RestaurantDto(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                image=restaurant.image.name,
                number_of_likes=restaurant.number_of_likes,
            ).get_dict()
            for restaurant in Restaurant.objects.all().annotate(
                number_of_likes=Count("likes")
            )
        ]

    def get_all_categories(self) -> QuerySet[RestaurantCategory]:
        return RestaurantCategory.objects.all()

    def like(self, request: HttpRequest) -> tuple[str, int]:
        try:
            data = loads(request.body)
        except JSONDecodeError:
            raise EmptyRequestBodyError("The request body cannot be empty")
        except TypeError:
            raise EmptyRequestBodyError("The request body cannot be empty")

        restaurant_id = data.get("restaurant_id")
        authenticated_user = cast(User, request.user)

        if not self.restaurant_exists(id=restaurant_id):
            raise RestaurantDoesNotExist(
                f"The restaurant with the id {restaurant_id} does not exist"
            )

        restaurant = self.get_by_id_queryset(id=restaurant_id)
        number_of_likes = restaurant.number_of_likes

        try:
            like = self.get_like(
                restaurant_id=restaurant_id, authenticated_user=authenticated_user
            )
            like.delete()
            action = "unliked"
            number_of_likes -= 1
        except:
            self.create_like(
                restaurant=restaurant, authenticated_user=authenticated_user
            )
            action = "liked"
            number_of_likes += 1

        return (action, number_of_likes)

    def get_by_id(self, id: str):
        restaurant = self.get_by_id_queryset(
            id, with_items=True, with_item_categories=True
        )

        return RestaurantDto(
            id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            image=restaurant.image.name,
            number_of_likes=restaurant.number_of_likes,
            food_items=[item for item in restaurant.items.all()],
            food_item_categories=[
                category for category in restaurant.item_categories.all()
            ],
        )

    def get_by_id_queryset(
        self, id: str, with_items=False, with_item_categories=False
    ) -> Restaurant:
        query = Restaurant.objects.all()

        if with_items:
            query = query.prefetch_related("items")
        if with_item_categories:
            query = query.prefetch_related("item_categories")

        return query.annotate(number_of_likes=Count("likes")).get(id=id)

    def restaurant_exists(self, id: str) -> bool:
        return Restaurant.objects.filter(id=id).exists()

    def get_like(self, restaurant_id: str, authenticated_user: User) -> RestaurantLike:
        return RestaurantLike.objects.get(
            restaurant__id=restaurant_id, user=authenticated_user
        )

    def create_like(self, restaurant: Restaurant, authenticated_user: User) -> None:
        RestaurantLike.objects.create(restaurant=restaurant, user=authenticated_user)

    def get_by_category(
        self, category_name: str | None
    ) -> list[dict[str, str | int | object]]:
        if not self.category_exists(category_name=category_name):
            raise RestaurantCategoryDoesNotExist()

        return [
            RestaurantDto(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                image=restaurant.image.name,
                number_of_likes=restaurant.likes.count(),
            ).get_dict()
            for restaurant in self.get_restaurants_by_category_queryset(
                category_name=category_name
            )
        ]

    def category_exists(self, category_name: str | None) -> bool:
        return RestaurantCategory.objects.filter(name=category_name).exists()

    def get_restaurants_by_category_queryset(
        self, category_name: str | None
    ) -> QuerySet[Restaurant]:
        return Restaurant.objects.filter(category__name=category_name)

    def get_items_by_category(self, category_name: str | None) -> list[dict]:
        try:
            category = RestaurantItemCategory.objects.get(name=category_name)

            return [item.get_dict() for item in category.items.all()]
        except ObjectDoesNotExist:
            raise RestaurantItemCategoryDoesNotExist()

    def get_item(self, id: str) -> RestaurantItem:
        return RestaurantItem.objects.get(id=id)

    def item_exists(self, id: str) -> bool:
        try:
            return RestaurantItem.objects.filter(id=id).exists()
        except:
            return False
