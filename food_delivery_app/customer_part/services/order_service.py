from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
import logging
from typing import cast

from ..dtos import OrderShowDto
from food_delivery_app.settings import DJANGO_ERROR_LOGGER
from ..models import Order, OrderItem, RestaurantItem
from ..services.cart_service import CartService
from ..services.restaurant_service import RestaurantService


class OrderService:
    cart_service: CartService

    def __init__(self) -> None:
        self.logger = logging.getLogger(DJANGO_ERROR_LOGGER)
        self.cart_service = CartService()

    def get_by_user(self, user_id: str):
        orders = Order.objects.filter(buyer__id=user_id).prefetch_related("items")

        return [
            OrderShowDto(
                date_ordered=order.created_at,
                order_items=order.items.select_related("item").all(),
                status=order.status,
            )
            for order in orders
        ]

    def create(self, request: HttpRequest):
        with transaction.atomic():
            transaction_savepoint = transaction.savepoint()

            try:
                order = self.create_order(user=cast(User, request.user))
                self.create_order_items(request=request, order=order)

                transaction.savepoint_commit(transaction_savepoint)
            except ValidationError as validation_error:
                error_messages = self.__get_error_messages(validation_error)
                self.log_errors(error_messages)

                transaction.savepoint_rollback(transaction_savepoint)

                raise Exception()

            self.clear_cart(request=request)

    def create_order(self, user: User) -> Order:
        order = Order()
        order.buyer = user

        order.save()

        return order

    def create_order_items(self, request: HttpRequest, order: Order) -> None:
        restaurant_service = RestaurantService()
        cart = self.cart_service.get_cart(request=request)

        for cart_item in cart["items"].values():
            restaurant_item = restaurant_service.get_item(id=cart_item["id"])
            self.create_order_item(
                order=order,
                restaurant_item=restaurant_item,
                quantity=cart_item["quantity"],
            )

    def create_order_item(
        self, order: Order, restaurant_item: RestaurantItem, quantity: int
    ) -> None:
        order_item = OrderItem()
        order_item.order = order
        order_item.item = restaurant_item
        order_item.quantity = quantity

        order_item.save()

    def clear_cart(self, request: HttpRequest) -> None:
        self.cart_service.clear_cart(request=request)

    def __get_error_messages(self, validation_error: ValidationError) -> str:
        """
        Formats all the validation error messages into a string.
        If the error_dict attribute exists the format is: "field_name: field_error_message\nfield_name: field_error_message"
        Otherwise the format can be any
        """

        if not hasattr(validation_error, "error_dict"):
            return str(validation_error.message)

        error_dict_items = list(validation_error.error_dict.items())
        error_messages_list = [
            f"{current_list[0]}: {validation_error.messages[index]}"
            for index, current_list in enumerate(error_dict_items)
        ]
        error_messages = "\n".join(error_messages_list)

        return error_messages

    def log_errors(self, error_messages: str) -> None:
        self.logger.error(error_messages)
