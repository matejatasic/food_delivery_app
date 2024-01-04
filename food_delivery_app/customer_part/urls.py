from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    index,
    address,
    login,
    register,
    logout_user,
    restaurant,
    restaurants,
    cart,
    orders,
    like,
    get_restaurants_by_category,
)


urlpatterns = [
    path("", index, name="home"),
    path("address", address, name="address"),
    path("cart", cart, name="cart"),
    path(
        "get_restaurants_by_category",
        get_restaurants_by_category,
        name="get_restaurants_by_category",
    ),
    path("like", like, name="like"),
    path("login", login, name="login"),
    path("logout", logout_user, name="logout"),
    path("orders", orders, name="orders"),
    path("register", register, name="register"),
    path("restaurant", restaurant, name="restaurant"),
    path("restaurants", restaurants, name="restaurants"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
