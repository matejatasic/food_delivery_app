from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import index, login, register, restaurant, restaurants, cart, orders


urlpatterns = [
    path("", index, name="home"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("restaurant", restaurant, name="restaurant"),
    path("restaurants", restaurants, name="restaurants"),
    path("cart", cart, name="cart"),
    path("orders", orders, name="orders"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
