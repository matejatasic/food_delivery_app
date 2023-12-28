from django.contrib import admin

from .models import Profile, Address, Restaurant, RestaurantCategory, RestaurantLike

# Register your models here.
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)
admin.site.register(RestaurantLike)
