from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from typing import Any
from unittest.mock import Mock


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(
        default="avatar.jpg", upload_to="profile_pictures", blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} profile"


class Address(BaseModel):
    latitude = models.FloatField()
    longitude = models.FloatField()
    raw = models.CharField(max_length=200)
    address_line = models.CharField(max_length=70, null=True, blank=True)
    district_1 = models.CharField()
    district_2 = models.CharField()
    country = models.CharField(max_length=60)
    locality = models.CharField(max_length=165)
    postal_code = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

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
