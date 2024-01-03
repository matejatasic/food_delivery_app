from django.db.models import (
    Model,
    DateTimeField,
    ForeignKey,
    OneToOneField,
    ImageField,
    CASCADE,
    SET_NULL,
    FloatField,
    CharField,
    IntegerField,
    TextField,
    DecimalField,
)
from django.contrib.auth.models import User
from django.utils import timezone
from typing import Any
from unittest.mock import Mock


class BaseModel(Model):
    created_at = DateTimeField(db_index=True, default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Add aditional functionality to the built in User authentication model
def liked_restaurants(self) -> list[int]:
    return [result[0] for result in self.likes.values_list("restaurant__id")]


User.add_to_class("liked_restaurants", liked_restaurants)


class Profile(BaseModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="profile")
    image = ImageField(
        default="avatar.jpg", upload_to="profile_pictures", blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} profile"


class Address(BaseModel):
    latitude = FloatField()
    longitude = FloatField()
    raw = CharField(max_length=200)
    address_line = CharField(max_length=70, null=True, blank=True)
    district_1 = CharField()
    district_2 = CharField()
    country = CharField(max_length=60)
    locality = CharField(max_length=165)
    postal_code = IntegerField(null=True, blank=True)
    user = ForeignKey(User, on_delete=CASCADE, related_name="addresses")

    def __str__(self) -> str:
        return self.raw

    def get_dict(self) -> dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "raw": self.raw,
            "address_line": self.address_line,
            "district_1": self.district_1,
            "district_2": self.district_2,
            "country": self.country,
            "locality": self.locality,
            "postal_code": self.postal_code,
            "user": self.user,
        }

    def get_mock(self) -> Mock:
        return Mock(spec=self)


class Restaurant(BaseModel):
    name = CharField(max_length=80)
    description = TextField()
    category = ForeignKey(
        "RestaurantCategory", on_delete=SET_NULL, null=True, related_name="restaurants"
    )
    image = ImageField(upload_to="restaurant_pictures")

    def __str__(self) -> str:
        return self.name


class RestaurantCategory(BaseModel):
    name = CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Restaurant categories"

    def __str__(self) -> str:
        return self.name


class RestaurantLike(BaseModel):
    restaurant = ForeignKey(Restaurant, on_delete=CASCADE, related_name="likes")
    user = ForeignKey(User, on_delete=CASCADE, related_name="likes")

    def __str__(self) -> str:
        return f"Like by {self.user.username} to {self.restaurant.name}"


class RestaurantItem(BaseModel):
    name = CharField(max_length=80)
    description = TextField()
    restaurant = ForeignKey(Restaurant, on_delete=CASCADE, related_name="items")
    price = DecimalField(max_digits=6, decimal_places=2)
