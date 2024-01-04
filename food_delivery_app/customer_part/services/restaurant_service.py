from django.contrib.auth.models import User
from django.db.models import QuerySet

from ..dtos import RestaurantDto
from ..exceptions import RestaurantDoesNotExist, RestaurantCategoryDoesNotExist
from ..models import Restaurant, RestaurantCategory, RestaurantLike


LIKED = "liked"
UNLIKED = "unliked"


class RestaurantService:
    def get_all(self) -> list[dict[str, str | int]]:
        return [
            RestaurantDto(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                image=restaurant.image.name,
                number_of_likes=restaurant.likes.count(),
            ).toDict()
            for restaurant in Restaurant.objects.all()
        ]

    def get_all_categories(self) -> QuerySet[RestaurantCategory]:
        return RestaurantCategory.objects.all()

    def like(self, restaurant_id: str, authenticated_user: User) -> tuple[str, int]:
        if not self.restaurant_exists(id=restaurant_id):
            raise RestaurantDoesNotExist()

        restaurant = self.get_by_id(id=restaurant_id)

        try:
            like = self.get_like(
                restaurant_id=restaurant_id, authenticated_user=authenticated_user
            )
            like.delete()
            action = "unliked"
        except:
            self.create_like(
                restaurant=restaurant, authenticated_user=authenticated_user
            )
            action = "liked"

        return (action, restaurant.likes.count())

    def get_by_id(self, id: str) -> Restaurant:
        return Restaurant.objects.get(id=id)

    def restaurant_exists(self, id: str) -> bool:
        return Restaurant.objects.filter(id=id).exists()

    def get_like(self, restaurant_id: str, authenticated_user: User) -> RestaurantLike:
        return RestaurantLike.objects.get(
            restaurant__id=restaurant_id, user=authenticated_user
        )

    def create_like(self, restaurant: Restaurant, authenticated_user: User) -> None:
        RestaurantLike.objects.create(restaurant=restaurant, user=authenticated_user)

    def get_by_category(self, category_name: str | None) -> list[dict[str, str | int]]:
        if not self.category_exists(category_name=category_name):
            raise RestaurantCategoryDoesNotExist()

        return [
            RestaurantDto(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                image=restaurant.image.name,
                number_of_likes=restaurant.likes.count(),
            ).toDict()
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
