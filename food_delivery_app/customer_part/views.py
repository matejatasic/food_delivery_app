from django.core.cache import cache
from django.core.exceptions import (
    PermissionDenied,
    BadRequest,
)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import Form, ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from http import HTTPStatus
from typing import cast

from .decorators import anonimity_required
from .forms import RegisterForm, LoginForm
from food_delivery_app.settings import STRIPE_API_PUBLIC_KEY
from .exceptions import (
    OrderDoesNotExist,
)
from .models import OrderStatus
from .services.cart_service import CartService
from .services.login_service import LoginService
from .services.order_service import OrderService
from .services.register_service import RegisterService
from .services.restaurant_service import RestaurantService


def index(request: HttpRequest) -> HttpResponse:
    restaurant_service = RestaurantService()

    most_liked_restaurants = cache.get(f"most-liked-restaurants")
    most_ordered_items = cache.get(f"most-ordered-items")

    if not most_liked_restaurants:
        most_liked_restaurants = restaurant_service.get_most_liked()
        cache.set("most-liked-restaurants", most_liked_restaurants, 900)

    if not most_ordered_items:
        most_ordered_items = restaurant_service.get_most_ordered_items()
        cache.set("most-ordered-items", most_ordered_items, 900)

    return render(
        request,
        "customer_part/home.html",
        {
            "most_liked_restaurants": most_liked_restaurants,
            "most_ordered_items": most_ordered_items,
        },
    )


@anonimity_required("home")
def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        login_service: LoginService = LoginService()
        form: Form = LoginForm(request.POST)

        try:
            login_service.login(request, form)

            GROUP_ROUTE_MAPPER = {
                "Admin": reverse("admin:index"),
                "Customer": reverse("home"),
                "Driver": reverse("current_deliveries"),
            }

            try:
                route = GROUP_ROUTE_MAPPER.get(request.user.groups.all()[0].name, reverse("home"))  # type: ignore
            except:
                route = reverse("home")

            return redirect(route)
        except ValidationError:
            return render(request, "customer_part/login.html", {"form": form})
        except PermissionDenied:
            return render(request, "customer_part/login.html", {"form": form})

    return render(request, "customer_part/login.html", {"form": LoginForm()})


@anonimity_required("home")
def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        register_service: RegisterService = RegisterService()
        form: ModelForm = RegisterForm(request.POST, request.FILES)

        try:
            register_service.register(request, form)

            return redirect(reverse("home"))
        except ValidationError:
            return render(request, "customer_part/register.html", {"form": form})

    return render(request, "customer_part/register.html", {"form": RegisterForm()})


@login_required(login_url="/login")  # type: ignore
def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)

    return redirect(reverse("home"))


def restaurant(request: HttpRequest, id: str) -> HttpResponse:
    restaurant_service = RestaurantService()
    restaurant = cache.get(f"restaurant-{id}")

    if not restaurant:
        restaurant = restaurant_service.get_by_id(id=id)
        cache.set(f"restaurant-{id}", restaurant, 900)

    cart_service = CartService()

    return render(
        request,
        "customer_part/restaurant.html",
        {"restaurant": restaurant, "cart": cart_service.get_cart(request=request)},
    )


def restaurants(request: HttpRequest) -> HttpResponse:
    restaurant_service = RestaurantService()

    restaurants_instances = cache.get("restaurants")
    categories = cache.get("restaurant-categories")

    if not restaurants_instances:
        restaurants_instances = restaurant_service.get_all()
        cache.set("restaurants", restaurants_instances, 900)

    if not categories:
        categories = restaurant_service.get_all_categories()
        cache.set("restaurant-categories", categories, 900)

    return render(
        request,
        "customer_part/restaurants.html",
        {
            "restaurants": restaurants_instances,
            "categories": categories,
        },
    )


@login_required(login_url="/login")  # type: ignore
def cart(request: HttpRequest) -> HttpResponse:
    cart_service = CartService()

    price_for_all_items, delivery, tax, total = cart_service.get_cart_expenses(
        request=request
    )

    return render(
        request,
        "customer_part/cart.html",
        {
            "cart": cart_service.get_cart(request),
            "price_for_all_items": price_for_all_items,
            "delivery": delivery,
            "tax": tax,
            "total": total,
            "stripe_public_key": STRIPE_API_PUBLIC_KEY,
        },
    )


@login_required(login_url="/login")  # type: ignore
def orders(request: HttpRequest) -> HttpResponse:
    order_service = OrderService()
    orders = cache.get(f"orders-{request.user.id}")

    if not orders:
        orders = order_service.get_by_user(cast(str, request.user.id))
        cache.set(f"orders-{request.user.id}", orders, 30)

    return render(request, "customer_part/orders.html", {"orders": orders})


@login_required(login_url="/login")  # type: ignore
def pending_orders(request: HttpRequest) -> HttpResponse:
    order_service = OrderService()
    orders = order_service.get_ordered()

    return render(
        request,
        "customer_part/drivers/pending_orders.html",
        {"orders": orders, "pending_status": OrderStatus.BEING_TRANSPORTED},
    )


@login_required(login_url="/login")  # type: ignore
def current_deliveries(request: HttpRequest) -> HttpResponse:
    order_service = OrderService()
    orders = order_service.get_by_driver(
        user_id=cast(str, request.user.id), status=OrderStatus.BEING_TRANSPORTED
    )

    return render(
        request,
        "customer_part/drivers/current_deliveries.html",
        {"orders": orders, "done_status": OrderStatus.DELIVERED},
    )


@login_required(login_url="/login")  # type: ignore
def finished_deliveries(request: HttpRequest) -> HttpResponse:
    order_service = OrderService()
    orders = order_service.get_by_driver(
        user_id=cast(str, request.user.id), status=OrderStatus.DELIVERED
    )

    return render(
        request,
        "customer_part/drivers/finished_deliveries.html",
        {"orders": orders, "done_status": OrderStatus.DELIVERED},
    )


def update_order(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "You are not authorized to perform this action"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    if request.method == "GET":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    order_service = OrderService()

    try:
        order_service.update(
            id=request.POST.get("id"),
            status=request.POST.get("status"),
            user_id=cast(int, request.user.id),
        )

        return redirect(reverse("current_deliveries"))
    except BadRequest as e:
        return render(
            request,
            "customer_part/error.html",
            {"title": "Bad Request", "message": str(e)},
        )
    except OrderDoesNotExist as e:
        return render(
            request,
            "customer_part/error.html",
            {"title": "Order does not exist", "message": str(e)},
        )


@login_required(login_url="/login")  # type: ignore
def checkout_return(request: HttpRequest):
    return render(
        request,
        "customer_part/return.html",
        {"session_id": request.GET.get("session_id")},
    )
