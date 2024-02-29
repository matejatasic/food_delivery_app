from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Unauthorized(Exception):
    """Access was denied to the requested resource or the operation"""

    pass


class InternalServerError(Exception):
    """There is an error on the server which received the request"""

    pass


class EmptyRequestBodyError(Exception):
    """The request body is empty"""


class AddressValidationError(ValidationError):
    """There is an error while creating the Address"""


class RestaurantDoesNotExist(ObjectDoesNotExist):
    """The Restaurant instance does not exist in the database"""


class RestaurantCategoryDoesNotExist(ObjectDoesNotExist):
    """The RestaurantCategory instance does not exist in the database"""


class RestaurantItemCategoryDoesNotExist(ObjectDoesNotExist):
    """The RestaurantItemCategory instance does not exist in the database"""


class RestaurantItemDoesNotExist(ObjectDoesNotExist):
    """The RestaurantItem instance does not exist in the database"""


class RestaurantItemNotInCart(ObjectDoesNotExist):
    """Restaurant item information is not present in the cart"""


class StripeTaxRateDoesNotExist(Exception):
    """The tax rate is not set"""


class OrderDoesNotExist(ObjectDoesNotExist):
    """The Order does not exist"""

class OrderStatusDoesNotExist(ObjectDoesNotExist):
    """The Order status does not exist"""
