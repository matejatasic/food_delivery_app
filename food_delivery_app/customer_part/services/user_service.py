from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import transaction
import logging

from ..exceptions import AddressValidationError
from food_delivery_app.settings import DJANGO_ERROR_LOGGER
from ..services.address_service import AddressService


class UserService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(DJANGO_ERROR_LOGGER)

    def create(
        self,
        username: str,
        password: str,
        first_name: str | None,
        last_name: str | None,
        email: str,
        address: dict | None,
    ) -> User:
        with transaction.atomic():
            transaction_savepoint = transaction.savepoint()

            user = self.get_model_instance(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.set_password(password)
            user.full_clean()
            user.save()

            if address:
                try:
                    self.create_address(
                        latitude=address["latitude"],
                        longitude=address["longitude"],
                        raw_address=address["raw"],
                        address_line=address["address_line"],
                        district_1=address["district_1"],
                        district_2=address["district_2"],
                        country=address["country"],
                        locality=address["locality"],
                        postal_code=address["postal_code"],
                        user=user,
                    )

                    transaction.savepoint_commit(transaction_savepoint)
                except ValidationError as validation_error:
                    error_messages = self.__get_error_messages(validation_error)
                    self.log_errors(error_messages)

                    transaction.savepoint_rollback(transaction_savepoint)

                    raise AddressValidationError(error_messages)

            return user

    def get_model_instance(
        self, username: str, first_name: str | None, last_name: str | None, email: str
    ) -> User:
        return User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

    def create_address(
        self,
        latitude: int,
        longitude: int,
        raw_address: str,
        address_line: str | None,
        district_1: str,
        district_2: str,
        country: str,
        locality: str,
        postal_code: str | None,
        user: User,
    ) -> None:
        address_service = self.get_address_service()

        address_service.create(
            latitude=latitude,
            longitude=longitude,
            raw_address=raw_address,
            address_line=address_line,
            district_1=district_1,
            district_2=district_2,
            country=country,
            locality=locality,
            postal_code=postal_code,
            user=user,
        )

    def get_address_service(self) -> AddressService:
        return AddressService()

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
