from django.core.cache import cache
from django.core.exceptions import (
    FieldDoesNotExist,
    FieldError,
    BadRequest,
)
from django.http import HttpRequest, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from http import HTTPStatus
from json import dumps
from stripe import InvalidRequestError

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
from .services.stripe_service import StripeService
from .services.cart_service import CartService
from .services.order_service import OrderService
from .services.restaurant_service import RestaurantService


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
        client_secret = stripe_service.create_checkout_session(cart=cart)

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
    session_id = request.GET.get("session_id")

    try:
        session = stripe_service.get_session(session_id=session_id)

        return JsonResponse(
            {"status": session.status, "customer_email": session.customer_details.email}  # type: ignore
        )
    except BadRequest as e:
        return JsonResponse(
            {"status": "failed", "message": str(e)}, status=HTTPStatus.BAD_REQUEST
        )
    except InvalidRequestError:
        return JsonResponse(
            {
                "status": "failed",
                "message": f"The session with the id {session_id} does not exist",
            },
            status=HTTPStatus.BAD_REQUEST,
        )
