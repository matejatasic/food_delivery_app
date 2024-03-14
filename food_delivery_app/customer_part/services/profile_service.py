from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
import logging
from typing import cast

from ..exceptions import AddressValidationError
from food_delivery_app.settings import DJANGO_ERROR_LOGGER
from ..models import Profile, Address
from ..services.address_service import AddressService
from ..types import AddressDictionary


class ProfileService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(DJANGO_ERROR_LOGGER)

    def create(
        self, user: User, image: InMemoryUploadedFile | None, address: AddressDictionary
    ) -> Profile:
        with transaction.atomic():
            transaction_savepoint = transaction.savepoint()

            try:
                address_instance: Address = self.create_address(
                    latitude=address["latitude"],
                    longitude=address["longitude"],
                    raw=address["raw"],
                    address_line=address["address_line"],
                    district_1=address["district_1"],
                    district_2=address["district_2"],
                    country=address["country"],
                    locality=address["locality"],
                    postal_code=address["postal_code"],
                )

                profile = self.get_model_instance(
                    user=user, image=image, address=address_instance
                )
                profile.full_clean()
                profile.save()

                transaction.savepoint_commit(transaction_savepoint)
            except ValidationError as validation_error:
                error_messages = self.__get_error_messages(validation_error)
                self.log_errors(error_messages)

                transaction.savepoint_rollback(transaction_savepoint)

                raise AddressValidationError(error_messages)

            return profile

    def get_model_instance(
        self, user: User, image: InMemoryUploadedFile | None, address: Address
    ) -> Profile:
        if image is None:
            image_str = "avatar.png"
        else:
            image_str = cast(str, image.name)

        return Profile(user=user, image=image_str, address=address)

    def create_address(
        self,
        latitude: int,
        longitude: int,
        raw: str,
        address_line: str | None,
        district_1: str,
        district_2: str,
        country: str,
        locality: str,
        postal_code: str | None,
    ) -> Address:
        address_service = self.get_address_service()

        return address_service.create(
            latitude=latitude,
            longitude=longitude,
            raw=raw,
            address_line=address_line,
            district_1=district_1,
            district_2=district_2,
            country=country,
            locality=locality,
            postal_code=postal_code,
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
