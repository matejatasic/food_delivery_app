from django.core.cache import cache
from django.core.exceptions import (
    PermissionDenied,
    FieldDoesNotExist,
    FieldError,
    BadRequest,
)
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import Form, ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from http import HTTPStatus
from json import dumps

from .decorators import anonimity_required
from .forms import RegisterForm, LoginForm
from food_delivery_app.settings import STRIPE_API_PUBLIC_KEY
from .exceptions import (
    RestaurantDoesNotExist,
    RestaurantCategoryDoesNotExist,
    RestaurantItemCategoryDoesNotExist,
    RestaurantItemDoesNotExist,
    RestaurantItemNotInCart,
    EmptyRequestBodyError,
    StripeTaxRateDoesNotExist,
)
from .services.address_service import AddressService
from .services.cart_service import CartService
from .services.login_service import LoginService
from .services.order_service import OrderService
from .services.register_service import RegisterService
from .services.restaurant_service import RestaurantService
from .services.stripe_service import StripeService


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


@login_required
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


def get_cart(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "You are not authorized to perform this action"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    if request.method == "POST":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    cart_service = CartService()

    price_for_all_items, delivery, tax, total = cart_service.get_cart_expenses(
        request=request
    )

    return JsonResponse(
        {
            "data": dumps(
                {
                    "cart": cart_service.get_cart(request),
                    "price_for_all_items": price_for_all_items,
                    "delivery": delivery,
                    "tax": tax,
                    "total": total,
                }
            )
        },
        status=HTTPStatus.OK,
    )


def create_order(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "You are not authorized to perform this action"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    if request.method == "GET":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.BAD_REQUEST)

    order_service = OrderService()

    try:
        order_service.create(request=request)

        return JsonResponse(
            {"message": "Sucessfully cleared the cart"},
            status=HTTPStatus.OK,
        )
    except Exception:
        return JsonResponse(
            {"message": "There was an error while creating the order"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


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


def create_checkout_session(request: HttpRequest):
    stripe_service = StripeService()
    cart_service = CartService()
    cart = cart_service.get_cart(request=request)

    try:
        client_secret = stripe_service.create_checkout_session(
            username=str(request.user.username), cart=cart
        )

        return JsonResponse({"clientSecret": client_secret})
    except StripeTaxRateDoesNotExist as e:
        return JsonResponse(
            {"error": "There was a server error, please try again later"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "There was a server error, please try again later"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def stripe_session_status(request: HttpRequest):
    stripe_service = StripeService()
    session = stripe_service.get_session(session_id=request.GET.get("session_id"))

    try:
        return JsonResponse(
            {"status": session.status, "customer_email": session.customer_details.email}  # type: ignore
        )
    except BadRequest as e:
        return JsonResponse({"status": "failed", "message": str(e)})


@login_required
def checkout_return(request: HttpRequest):
    return render(
        request,
        "customer_part/return.html",
        {"session_id": request.GET.get("session_id")},
    )
