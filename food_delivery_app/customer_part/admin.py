from django.contrib import admin

from .models import (
    Profile,
    Address,
    Restaurant,
    RestaurantCategory,
    RestaurantLike,
    RestaurantItem,
    RestaurantItemCategory,
    Order,
    OrderItem,
)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)
admin.site.register(RestaurantLike)
admin.site.register(RestaurantItem)
admin.site.register(RestaurantItemCategory)
admin.site.register(Order)
admin.site.register(OrderItem)
