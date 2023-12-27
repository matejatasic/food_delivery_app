from django.db.models import QuerySet

from ..models import Restaurant, RestaurantCategory


class RestaurantService:
    def get_all(self) -> QuerySet[Restaurant]:
        return Restaurant.objects.all()

    def get_all_categories(self):
        return RestaurantCategory.objects.all()
