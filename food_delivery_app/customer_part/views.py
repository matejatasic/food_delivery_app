from django.core.cache import cache
from django.core.exceptions import PermissionDenied, FieldDoesNotExist, FieldError
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import Form, ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from http import HTTPStatus
from json import dumps

from .decorators import anonimity_required
from .forms import RegisterForm, LoginForm
from .exceptions import (
    RestaurantDoesNotExist,
    RestaurantCategoryDoesNotExist,
    RestaurantItemCategoryDoesNotExist,
    RestaurantItemDoesNotExist,
    RestaurantItemNotInCart,
    EmptyRequestBodyError,
)
from .services.address_service import AddressService
from .services.cart_service import CartService
from .services.login_service import LoginService
from .services.register_service import RegisterService
from .services.restaurant_service import RestaurantService

# cache the page for 6 hours
@cache_page(21600)
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/home.html")


@anonimity_required("home")
def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        login_service: LoginService = LoginService()
        form: Form = LoginForm(request.POST)

        try:
            login_service.login(request, form)

            return redirect(reverse("home"))
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


@login_required
def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)

    return redirect(reverse("home"))

def restaurant(request: HttpRequest, id: str) -> HttpResponse:
    restaurant_service = RestaurantService()
    restaurant = cache.get(f"restaurant-{id}")

    if not restaurant:
        restaurant = restaurant_service.get_by_id(id=id)
        cache.set(f"restaurant-{id}", restaurant, 900)

    return render(request, "customer_part/restaurant.html", {"restaurant": restaurant})

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


def cart(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/cart.html")


def orders(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/orders.html")


def address(request: HttpRequest) -> JsonResponse:
    address_service = AddressService()
    addresses: list[dict[str, str]] = address_service.get_address_options(
        request.GET["term"]
    )

    return JsonResponse(
        {
            "results": addresses,
        },
        encoder=DjangoJSONEncoder,
    )


def like(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "You are not authorized to perform this action"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    if request.method == "GET":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    restaurant_service = RestaurantService()

    try:
        action_taken, current_number_of_likes = restaurant_service.like(request=request)

        return JsonResponse(
            {
                "message": f"The post was {action_taken}",
                "action": action_taken,
                "current_number_of_likes": current_number_of_likes,
            },
            status=HTTPStatus.OK,
        )
    except EmptyRequestBodyError as error:
        return JsonResponse({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
    except RestaurantDoesNotExist as error:
        return JsonResponse(
            {"error": str(error)},
            status=HTTPStatus.NOT_FOUND,
        )


def change_cart(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "You are not authorized to perform this action"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    if request.method == "GET":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    cart_service = CartService()

    try:
        item_name, total_number_of_items = cart_service.add_item(request=request)

        return JsonResponse(
            {
                "data": dumps(
                    {
                        "item_name": item_name,
                        "total_number_of_items": total_number_of_items,
                    }
                ),
            },
            status=HTTPStatus.OK,
        )
    except EmptyRequestBodyError as error:
        return JsonResponse({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
    except FieldDoesNotExist as error:
        return JsonResponse({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
    except FieldError as error:
        return JsonResponse({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
    except RestaurantItemDoesNotExist as error:
        return JsonResponse({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)
    except RestaurantItemNotInCart as error:
        return JsonResponse({"error": str(error)}, status=HTTPStatus.BAD_REQUEST)


def get_restaurants_by_category(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    category_name = request.GET.get("category_name")
    restaurant_service = RestaurantService()

    try:
        restaurants_instances = cache.get(f"restaurant-{category_name}")

        if not restaurants_instances:
            restaurants_instances = restaurant_service.get_by_category(category_name)
            cache.set(f"restaurant-{category_name}", restaurants_instances, 900)

        return JsonResponse(
            {
                "data": dumps(restaurants_instances),
            },
            status=HTTPStatus.OK,
        )
    except RestaurantCategoryDoesNotExist:
        return JsonResponse(
            {"error": f"The restaurant category {category_name} does not exist"},
            status=HTTPStatus.NOT_FOUND,
        )


def get_restaurant_items_by_category(request):
    if request.method == "POST":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    category_name = request.GET.get("category_name")
    restaurant_service = RestaurantService()

    try:
        items = cache.get(f"restaurant-item-{category_name}")

        if not items:
            items = restaurant_service.get_items_by_category(category_name)
            cache.set(f"restaurant-item-{category_name}", items, 900)

        return JsonResponse(
            {
                "data": dumps(items),
            },
            status=HTTPStatus.OK,
        )
    except RestaurantItemCategoryDoesNotExist:
        return JsonResponse(
            {"error": f"The item category {category_name} does not exist"},
            status=HTTPStatus.NOT_FOUND,
        )
