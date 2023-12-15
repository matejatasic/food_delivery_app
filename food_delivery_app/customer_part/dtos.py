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
