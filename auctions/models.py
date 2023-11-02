from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", null=True, blank=True)
 
class Category(models.Model):
    title = models.CharField(max_length=64, blank=False)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = "Categories"

class Listing(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    starting_price = models.IntegerField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    image = models.CharField(blank=True, max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="bids")
    amount = models.IntegerField(blank=False)

    def __str__(self) -> str:
        return f"A bid by {self.user.username} for {self.listing.title}"

class Comment(models.Model):
    comment = models.TextField(blank=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        return f"A comment by {self.user.username} for {self.listing.title}"