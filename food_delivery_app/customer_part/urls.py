from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("restaurant", views.restaurant, name="restaurant"),
    path("restaurants", views.restaurants, name="restaurants"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders")
]