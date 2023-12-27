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
    BooleanField,
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


class RestaurantCategory(BaseModel):
    name = CharField(max_length=50)


class RestaurantLikes(BaseModel):
    restaurant = ForeignKey(Restaurant, on_delete=CASCADE, related_name="likes")
    user = ForeignKey(User, on_delete=CASCADE, related_name="likes")
    is_dislike = BooleanField()
