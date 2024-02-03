from .base import BASE_DIR

DJANGO_ERROR_LOGGER = "django_error"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module}:\n{message}\n{pathname}, line {lineno}, in {funcName}\n",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/error.log",
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        DJANGO_ERROR_LOGGER: {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        }
    },
}
