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
    get_cart,
    get_restaurants_by_category,
    get_restaurant_items_by_category,
    change_cart,
    create_checkout_session,
    stripe_session_status,
    checkout_return,
    create_order,
    pending_orders,
    driver,
    assign_order,
)


urlpatterns = [
    path("", index, name="home"),
    path("address", address, name="address"),
    path("assign_order", assign_order, name="assign_order"),
    path("cart", cart, name="cart"),
    path("change_cart", change_cart, name="change_cart"),
    path(
        "checkout_return",
        checkout_return,
        name="checkout_return",
    ),
    path("create_order", create_order, name="create_order"),
    path(
        "create_checkout_session",
        create_checkout_session,
        name="create_checkout_session",
    ),
    path("driver", driver, name="driver"),
    path("pending_orders", pending_orders, name="pending_orders"),
    path("get_cart", get_cart, name="get_cart"),
    path(
        "get_restaurants_by_category",
        get_restaurants_by_category,
        name="get_restaurants_by_category",
    ),
    path(
        "get_restaurant_items_by_category",
        get_restaurant_items_by_category,
        name="get_restaurant_items_by_category",
    ),
    path("like", like, name="like"),
    path("login", login, name="login"),
    path("logout", logout_user, name="logout"),
    path("orders", orders, name="orders"),
    path("register", register, name="register"),
    path("restaurant/<int:id>", restaurant, name="restaurant"),
    path("restaurants", restaurants, name="restaurants"),
    path(
        "stripe_session_status",
        stripe_session_status,
        name="stripe_session_status",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
