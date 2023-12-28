from django.contrib.auth.models import User
from django.db.models import QuerySet

from ..exceptions import RestaurantDoesNotExist
from ..models import Restaurant, RestaurantCategory, RestaurantLike


class RestaurantService:
    def get_all(self) -> QuerySet[Restaurant]:
        return Restaurant.objects.all()

    def get_all_categories(self) -> QuerySet[RestaurantCategory]:
        return RestaurantCategory.objects.all()

    def like(self, restaurant_id: str, authenticated_user: User) -> tuple[str, int]:
        if not Restaurant.objects.filter(id=restaurant_id).exists():
            raise RestaurantDoesNotExist()

        restaurant = Restaurant.objects.get(id=restaurant_id)
        try:
            like = RestaurantLike.objects.get(
                restaurant__id=restaurant_id, user=authenticated_user
            )
            like.delete()
            action = "unliked"
        except:
            RestaurantLike.objects.create(
                restaurant=restaurant, user=authenticated_user
            )
            action = "liked"

        return (action, restaurant.likes.count())
