from django.core.exceptions import BadRequest
import logging

from ..dtos import AddressOptionDto
from ..exceptions import Unauthorized, InternalServerError
from food_delivery_app.settings import DJANGO_ERROR_LOGGER
from ..dtos import MapsResponseResourcesDto
from ..models import Address, User
from ..services.maps_service import MapsService


class AddressService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(DJANGO_ERROR_LOGGER)
        self.maps_service = MapsService()

    def get_address_options(self, query: str) -> list[dict[str, str]]:
        try:
            addresses_resouces: list[
                MapsResponseResourcesDto
            ] = self.maps_service.get_location_by_query(query)

            addresses: list[dict[str, str]] = []

            for address in addresses_resouces:
                address_instance = Address(
                    latitude=address.latitude,
                    longitude=address.longitude,
                    raw=address.formatted_address,
                    address_line=address.address_line,
                    district_1=address.district_1,
                    district_2=address.district_2,
                    country=address.country_region,
                    locality=address.locality,
                    postal_code=address.postal_code,
                )
                address_dto = AddressOptionDto(address_instance)

                addresses.append(address_dto.toDict())

            return addresses
        except BadRequest as e:
            self.logger.error(e)

            return []
        except Unauthorized as e:
            self.logger.error(e)

            return []
        except InternalServerError as e:
            self.logger.error(e)

            return []
        except Exception as e:
            self.logger.error(e)

            return []
