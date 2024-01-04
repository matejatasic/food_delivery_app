from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Unauthorized(Exception):
    """Access was denied to the requested resource or the operation"""

    pass


class InternalServerError(Exception):
    """There is an error on the server which received the request"""

    pass


class AddressValidationError(ValidationError):
    """There is an error while creating the Address"""


class RestaurantDoesNotExist(ObjectDoesNotExist):
    """The Restaurant instance does not exist in the database"""


class RestaurantCategoryDoesNotExist(ObjectDoesNotExist):
    """The RestaurantCategory instance does not exist in the database"""
