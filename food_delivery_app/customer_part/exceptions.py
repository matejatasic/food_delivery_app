class Unauthorized(Exception):
    """Access was denied to the requested resource or the operation"""

    pass


class InternalServerError(Exception):
    """There is an error on the server which received the request"""

    pass
