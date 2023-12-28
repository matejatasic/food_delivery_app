from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    index,
    addresses,
    login,
    register,
    logout_user,
    restaurant,
    restaurants,
    cart,
    orders,
    like,
)


urlpatterns = [
    path("", index, name="home"),
    path("addresses", addresses, name="addresses"),
    path("cart", cart, name="cart"),
    path("like", like, name="like"),
    path("login", login, name="login"),
    path("logout", logout_user, name="logout"),
    path("orders", orders, name="orders"),
    path("register", register, name="register"),
    path("restaurant", restaurant, name="restaurant"),
    path("restaurants", restaurants, name="restaurants"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
