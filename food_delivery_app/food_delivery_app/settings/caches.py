import sys

from .base import DEBUG
from .base import os

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_LOCATION", "redis://127.0.0.1:6379"),
        "OPTIONS": {
            "DB": 0,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 0 if DEBUG else 300,
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_LOCATION", "redis://127.0.0.1:6379"),
        "OPTIONS": {
            "DB": 1,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

if "test" in sys.argv:
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
