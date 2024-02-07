from django.core.exceptions import BadRequest
from django.urls import reverse
import logging
import stripe
from typing import cast

from ..exceptions import StripeTaxRateDoesNotExist
from food_delivery_app.settings import (
    STRIPE_API_SECRET_KEY,
    STRIPE_TAX_RATE,
    SITE_DOMAIN,
    MEDIA_URL,
    DJANGO_ERROR_LOGGER,
)
from ..types import Cart, CartItemsDictionary

stripe.api_key = STRIPE_API_SECRET_KEY


class StripeService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(DJANGO_ERROR_LOGGER)

    def create_checkout_session(self, cart: Cart) -> str | None:
        if not STRIPE_TAX_RATE:
            self.log_errors("The TAX_RATE environment variable is not set")
            raise StripeTaxRateDoesNotExist()

        try:
            session = self.create_session(cart=cart)

            return session.client_secret
        except stripe.InvalidRequestError as error:
            self.log_errors(error=error)
            raise Exception()

    def create_session(self, cart: Cart) -> stripe.checkout.Session:
        return stripe.checkout.Session.create(
            ui_mode="embedded",
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {
                            "amount": int(cart["delivery"] * 100),
                            "currency": "usd",
                        },
                        "display_name": "Delivery",
                    },
                },
            ],
            line_items=self.get_line_items(
                items=cast(CartItemsDictionary, cart["items"])
            ),
            mode="payment",
            return_url=f"{SITE_DOMAIN}{reverse('checkout_return')}"
            + "?session_id={CHECKOUT_SESSION_ID}",
        )

    def get_line_items(
        self, items: CartItemsDictionary
    ) -> list[stripe.checkout.Session.CreateParamsLineItem]:
        return [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item["name"],
                        "description": item["description"],
                        "images": [f"{SITE_DOMAIN}{MEDIA_URL}{item['image']}"],
                    },
                    "unit_amount": int(item["price"] * 100),
                },
                "quantity": item["quantity"],
                "tax_rates": [cast(str, STRIPE_TAX_RATE)],
            }
            for item in items.values()
        ]

    def get_session(self, session_id: str | None) -> stripe.checkout.Session:
        if session_id is None:
            raise BadRequest("Session id is missing")

        return self.retrieve_session(session_id=session_id)

    def retrieve_session(self, session_id: str):
        return stripe.checkout.Session.retrieve(session_id)

    def log_errors(self, error: Exception | str) -> None:
        self.logger.error(error)
