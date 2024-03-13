from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .api import (
    address,
    like,
    get_cart,
    get_restaurants_by_category,
    get_restaurant_items_by_category,
    change_cart,
    create_checkout_session,
    create_order,
    stripe_session_status,
)
from .views import (
    index,
    login,
    register,
    logout_user,
    restaurant,
    restaurants,
    cart,
    orders,
    checkout_return,
    pending_orders,
    current_deliveries,
    update_order,
    finished_deliveries,
)


urlpatterns = [
    path("", index, name="home"),
    path("address", address, name="address"),
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
    path("current_deliveries", current_deliveries, name="current_deliveries"),
    path("finished_deliveries", finished_deliveries, name="finished_deliveries"),
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
    path("update_order", update_order, name="update_order"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
