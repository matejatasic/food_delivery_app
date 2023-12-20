from django.core.serializers import serialize

from .models import Address


class AddressOptionDto:
    def __init__(self, address: Address) -> None:
        self.__address_model = address
        self.__address = address.raw

    def toDict(self):
        return {"id": serialize("json", [self.__address_model]), "text": self.__address}

    @property
    def pk(self):
        return self.__address_model

    @property
    def address(self):
        return self.__address

    def __str__(self) -> str:
        return self.__address


class MapsResponseResourcesDto:
    __bbox: list[int]
    __address: "MapsResponseAddressDto"

    def __init__(self, bbox: list[int], address_information: dict) -> None:
        self.__bbox = bbox
        self.__address = MapsResponseAddressDto(
            formatted_address=address_information["formattedAddress"],
            address_line=address_information.get("addressLine", None),
            district_1=address_information["adminDistrict"],
            district_2=address_information["adminDistrict2"],
            country_region=address_information["countryRegion"],
            locality=address_information["locality"],
            postal_code=address_information.get("postalCode", None),
        )

    @property
    def latitude(self):
        return self.__bbox[0]

    @property
    def longitude(self):
        return self.__bbox[1]

    @property
    def formatted_address(self):
        return self.__address.formatted_address

    @property
    def address_line(self) -> str | None:
        return self.__address.address_line

    @property
    def district_1(self) -> str:
        return self.__address.district_1

    @property
    def district_2(self) -> str:
        return self.__address.district_2

    @property
    def country_region(self) -> str:
        return self.__address.country_region

    @property
    def locality(self) -> str:
        return self.__address.locality

    @property
    def postal_code(self) -> str | None:
        return self.__address.postal_code


class MapsResponseAddressDto:
    __formatted_address: str
    __address_line: str | None
    __district_1: str
    __district_2: str
    __country_region: str
    __locality: str
    __postal_code: str | None

    def __init__(
        self,
        formatted_address: str,
        address_line: str | None,
        district_1: str,
        district_2: str,
        country_region: str,
        locality: str,
        postal_code: str | None,
    ) -> None:
        self.__formatted_address = formatted_address
        self.__address_line = address_line
        self.__district_1 = district_1
        self.__district_2 = district_2
        self.__country_region = country_region
        self.__locality = locality
        self.__postal_code = postal_code

    @property
    def formatted_address(self) -> str:
        return self.__formatted_address

    @property
    def address_line(self) -> str | None:
        return self.__address_line

    @property
    def district_1(self) -> str:
        return self.__district_1

    @property
    def district_2(self) -> str:
        return self.__district_2

    @property
    def country_region(self) -> str:
        return self.__country_region

    @property
    def locality(self) -> str:
        return self.__locality

    @property
    def postal_code(self) -> str | None:
        return self.__postal_code
