from .base import os

BING_MAPS_API_KEY = os.getenv("BING_MAPS_API_KEY")

CRISPY_TEMPLATE_PACK = "bootstrap5"

INTERNAL_IPS = os.getenv("ALLOWED_HOSTS", default="127.0.0.1").split(" ")

SELECT2_CACHE_BACKEND = "select2"

STRIPE_API_PUBLIC_KEY = os.getenv("STRIPE_API_PUBLIC_KEY")
STRIPE_API_SECRET_KEY = os.getenv("STRIPE_API_SECRET_KEY")
STRIPE_TAX_RATE = os.getenv("TAX_RATE")
